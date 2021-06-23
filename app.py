from web3 import Web3
from web3.auto import w3
from time import sleep
from decouple import config
from threading import Thread
from wtforms import SubmitField
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, redirect, url_for, flash, Markup, Response, jsonify
import json, binascii, requests, glob, qrcode, time
import utils.Import_PrivateKey as imPri
import utils.Mnemonic_util as imMnemonic
import utils.Pydenticon_Generator as pyIcon
import utils.Mnemonic_Scalping as mnemonic_Scalp
import utils.Ether_Transaction_Query as etherQuery

# Global variables
Stop_Threads = False
API_URL = config('ETHSCAN_URL')
ACCOUNT_KEY = config('KEY')
ACCOUNT_FILE = config('KEY_FILE')
KEY_BASE = config('KEYSTORE_BASE')
KFILE_HOME = config('KEYFILE_HOME')
NETWORK_HOME = config('NETWORK_NAME_DEV') 
_global_principal_address = ''
_global_recipient_address = ''
_global_wallet_address_counts = 0
_global_wallet_addresses = []
_global_wallet_balances = []
_global_wallet_balance_ether = []
_global_wallet_balance_usd = []
_recipient_wallet_addresses = []
_recipient_wallet_balance_ether = []
_recipient_wallet_balance_usd = []


# Connection Verification
web3 = Web3(Web3.HTTPProvider(NETWORK_HOME))
# print("Established_Connections :", web3.isConnected())
# print("Current_Block # :", web3.eth.blockNumber, "\n")


# Get the current USD price of cryptocurrency conversion from API URL
apiReq = requests.get(API_URL)
USD_CURRENT_PRICE=json.loads(apiReq.content)["USD"] 


# Function to return balances of ethereum
def toEther(balance):    
    return web3.fromWei(balance, 'ether')


# Function to return USD conversion values
def toUSD(balance):
    usd_sum = round(USD_CURRENT_PRICE * float(toEther(balance)), 2)    
    return usd_sum


# Function to return Trans USD conversion values
def toTransUSD(balance):
    usd_trans_sum = USD_CURRENT_PRICE * float(balance)          
    return str(usd_trans_sum)[:str(usd_trans_sum).index(".") + 3] 


# Function to generate account images
def accountImageCreation(account_address):    
    # Identicon Setup the padding(top, bottom, left, right) in pixels.
    padding = (10, 10, 10, 10)
    identicon_png = pyIcon.generator.generate(account_address, 20, 20, padding=padding, output_format="png")
    # Identicon can be easily saved to a file.
    f = open("static/images/%s.png" % (account_address), "wb")
    f.write(identicon_png)
    f.close()
    #Creating an instance of QRCode image
    qr = qrcode.QRCode(version=1, box_size=5, border=5)
    qr.add_data(account_address)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save('static/images/%s_qrcode.png' % (account_address))  


# Function to extract all accounts from geth
def extractAccounts():     
    # Change the glob if you want to only look through files with specific names
    files = glob.glob(f'{KFILE_HOME}/*', recursive=True)

    # clearing the lists
    _global_wallet_addresses.clear()            
    _global_wallet_balances.clear()            
    _global_wallet_balance_ether.clear()       
    _global_wallet_balance_usd.clear()          

    # Loop through multiple files    
    for idx, single_file in enumerate(files):
        with open(single_file, 'r') as sf:            
            json_file = json.load(sf)                 
            global _global_wallet_address_counts                   
            _global_wallet_addresses.insert(idx, web3.toChecksumAddress(json_file["address"]))                        
            _global_wallet_address_counts += 1
            sf.close()                        
        with open(single_file, 'r') as keyfile: 
            _encrypted_key = keyfile.read()             
            _global_wallet_balances.insert(idx, web3.eth.getBalance(_global_wallet_addresses[idx]))
            _global_wallet_balance_ether.insert(idx, str(toEther(_global_wallet_balances[idx])))
            _global_wallet_balance_usd.insert(idx, toUSD(_global_wallet_balances[idx]))                      
            keyfile.close()
    
    return _global_wallet_addresses, _global_wallet_balance_ether, _global_wallet_balance_usd


# Function to extract principal account cipher
def extractPrincipalCipher(principalAddress):     
    # Local Lists variables
    _principal_addresses_cipher = ''
    _local_principal_addresses = []
    _local_principal_addresses_cipher = []    

    # Change the glob if you want to only look through files with specific names
    files = glob.glob(f'{KFILE_HOME}/*', recursive=True)
    
    # Loop through multiple files    
    for idx, single_file in enumerate(files):
        with open(single_file, 'r') as sf:            
            json_file = json.load(sf)                                             
            _local_principal_addresses.insert(idx, web3.toChecksumAddress(json_file["address"]))                                              
            sf.close()
        with open(single_file, 'r') as keyfile: 
            _encrypted_key = keyfile.read()                         
            _local_principal_addresses_cipher.insert(idx, binascii.b2a_hex(w3.eth.account.decrypt(_encrypted_key, ACCOUNT_KEY)).decode('ascii')) 
            keyfile.close()
        if(str(principalAddress) == str(_local_principal_addresses[idx])): _principal_addresses_cipher = _local_principal_addresses_cipher[idx]            
        
    return _principal_addresses_cipher


# Fucntion to calling account and printing all accounts' balances
def listAccounts():
    # clearing the lists
    _recipient_wallet_addresses.clear()            
    _recipient_wallet_balance_ether.clear()
    _recipient_wallet_balance_usd.clear()
    for idx, account in enumerate(web3.eth.accounts):
        _recipient_wallet_addresses.insert(idx, account)
        _recipient_wallet_balance_ether.insert(idx, str(toEther(web3.eth.getBalance(account))))
        _recipient_wallet_balance_usd.insert(idx, toUSD(web3.eth.getBalance(account)))
        # print(f'[{idx+1}] Balance of {account} : {toEther(web3.eth.getBalance(account))} ETH')

    return _recipient_wallet_addresses, _recipient_wallet_balance_ether, _recipient_wallet_balance_usd


# Function to transfer web ethereum
def sendWebEther(reci_addr, donor_addr, amounts):    
          
    # get the nounce
    nonce = web3.eth.getTransactionCount(donor_addr)

    # build a transaction
    tx = {
        'nonce': nonce,
        'to': reci_addr,        
        'value': web3.toWei(amounts, 'ether'),
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei')
    }
    
    # sign a transaction    
    signed_tx = web3.eth.account.signTransaction(tx, extractPrincipalCipher(donor_addr))    

    # send a transaction
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    # decodes the transaction data 
    Tx_Status = web3.eth.getTransactionReceipt(tx_hash)['status']
    Tx_Num = web3.toHex(tx_hash)
    Frome = web3.eth.getTransactionReceipt(tx_hash)['from']
    To = web3.eth.getTransactionReceipt(tx_hash)['to']
    Wei_Amount = web3.eth.getTransaction(tx_hash)['value']
    Eth_Amount = toEther(web3.eth.getTransaction(tx_hash)['value'])
    Usd_Amount = toTransUSD(toEther(web3.eth.getTransaction(tx_hash)['value']))
    Gas_Fees_Wei = web3.eth.getTransaction(tx_hash)['gasPrice']
    Gas_Fees_Eth = '{:.8f}'.format(toEther(web3.eth.getTransaction(tx_hash)['gasPrice']))    
    Gas_Used = web3.eth.getTransactionReceipt(tx_hash)['gasUsed']    
    Block_Number = web3.eth.getTransactionReceipt(tx_hash)['blockNumber']    

    return Tx_Status, Tx_Num, Frome, To, Wei_Amount, Eth_Amount, Usd_Amount, Gas_Fees_Wei, Gas_Fees_Eth, Gas_Used, Block_Number


# Function of Tx results data 
def txResultData(tx_result):
    if(tx_result[0] == 1):              
        message = Markup(f'The transaction was successful for receipts.<br>Transaction Number: {tx_result[1]}<br>From: {tx_result[2]}<br>To: {tx_result[3]}<br>Transaction Amount: {tx_result[4]} Wei = {tx_result[5]} ETH = {tx_result[6]} $USD<br>GasPrice: {tx_result[7]} Wei = {tx_result[8]} ETH<br>GasUsed: {tx_result[9]}<br>Block Number: {tx_result[10]}') 
        flash(message, 'txResults') 
    else:
        message = "The transaction was failed and reverted by EVM."
        flash(message, 'txResults') 


# Function of PrivateKey import result display
def importResultData(import_result_code, import_result_stdout):    
    if(import_result_code == 0):     
        message = Markup(f'A private key has imported successfully.<br> {import_result_stdout}<br>') 
        flash(message, 'importResult')
    else:        
        message = Markup(f'{import_result_stdout}<br> Unable to import a private key. Please check a privatekey file and try again.<br>')
        flash(message, 'importResult') 


# Function to Retrieve Tx results historical data
def txResultHistoryData(query_file, start_block, end_block, principal_address):
    # Local Lists variables 
    _local_listLength = 0    
    _local_From = []
    _local_To = []
    _local_EthValue = []
    _local_USDValue = []
    _local_Nonce = []
    _local_BlockNumber = []
    _local_Hash = []
    _local_BlockHash = []            

    # Reading from JSON file   
    with open(etherQuery.queryEther(query_file, start_block, end_block, principal_address), 'r') as dataContent:        
            loaded_json = json.load(dataContent)    

            for idx, key in enumerate(loaded_json):                
                _local_From.insert(idx, loaded_json[idx]['from']) 
                _local_To.insert(idx, loaded_json[idx]['to'])
                _local_EthValue.insert(idx, toEther(loaded_json[idx]['value']))
                _local_USDValue.insert(idx, toUSD(loaded_json[idx]['value']))
                _local_Nonce.insert(idx, loaded_json[idx]['nonce'])
                _local_BlockNumber.insert(idx, loaded_json[idx]['blockNumber'])
                _local_Hash.insert(idx, loaded_json[idx]['hash'])
                _local_BlockHash.insert(idx, loaded_json[idx]['blockHash'])               
            _local_listLength = len(_local_From)
    dataContent.close()

    return _local_listLength, _local_From, _local_To, _local_EthValue, _local_USDValue, _local_Nonce, _local_BlockNumber, _local_Hash, _local_BlockHash


# Function to trigger Mnemonic Scalping Process
def triggerMnemonicScalp(stop_status):
    importedCount = 1        
    while True:
        global Stop_Threads                
        mnemonic_Scalp.importSeedPhraseInput(importedCount)                
        sleep(3)
        importedCount+=1        
        if stop_status():
            break

# Implement Flask WTForms
class PowerState(FlaskForm):
    state = SubmitField('ON')


# Flask http web display
app = Flask(__name__)
Bootstrap(app)
app.config['FLASK_ENV'] = 'development'
app.config['SECRET_KEY'] = 'abcd1234$'
app.config["TEMPLATES_AUTO_RELOAD"] = True
# Limit the size of upload file to 2 megabytes and application will refuse it.
app.config['MAX_CONTENT_LENGTH'] = 2*1024*1024

@app.route('/')
def index():    
    return render_template('index.html')

@app.errorhandler(413)
def error413(e):        
    return "A transmitted upload file exceeds the capacity limits(2MB). <br><br> <a href='/'>Go back to Main Page</a>", 413

@app.route('/AccountDashBoard', methods=['GET', 'POST'])
def AccountDashBoard():    
    account_name = extractAccounts()
    dataLen = len(account_name[0])    
    current_block = web3.eth.blockNumber
    # print(account_name)        
    return render_template('account_main.html', value0=account_name, value1=dataLen, value2=current_block)    
        
@app.route('/selectPrincipalData', methods=['POST'])
def selectPrincipalInput():
    global _global_principal_address    
    _global_principal_address = request.form['principle']
    accountImageCreation(_global_principal_address)
    recipientLists = listAccounts()    
    dataLen = len(recipientLists[0])                    
    return render_template('recipient_display.html', value0=_global_principal_address, value1=recipientLists, value2=dataLen)

@app.route('/queryPrincipalData', methods=['POST'])
def queryPrincipalInput():
    global _global_principal_address    
    _global_principal_address = request.form['principle']    
    accountImageCreation(_global_principal_address)    
    start_block = int(request.form['fromBlk'])
    end_block = int(request.form['toBlk']) + 1
    listLength, From, To, EthValue, USDValue, Nonce, BlockNumber, Hash, BlockHash = txResultHistoryData(_global_principal_address, start_block, end_block, _global_principal_address)           
    return render_template('query_display.html', value0=_global_principal_address, value1=start_block, value2=end_block, value3=listLength, value4=From, value5=To, value6=EthValue, value7=USDValue, value8=Nonce, value9=BlockNumber, value10=Hash, value11=BlockHash)

@app.route('/importPrivateKey', methods=['POST'])
def importPrivateKeyInput():    
    privateKeyValue = request.form['inputPrivateKey']        
    returncode, stdout = imPri.importPrivateKey(privateKeyValue) 
    importResultData(returncode, stdout)
    return redirect(url_for('AccountDashBoard'))

@app.route('/importSeedPhrase', methods=['POST'])
def importSeedPhraseInput():    
    seedPhraseValue = request.form['inputSeedPhrase']                
    biPrivateKey = imMnemonic.mnemonic_to_private_key(seedPhraseValue)    
    # print("Your private key is: {}".format(str(binascii.hexlify(biPrivateKey), 'utf-8')))
    privateKeyValue = format(str(binascii.hexlify(biPrivateKey), 'utf-8'))    
    returncode, stdout = imPri.importPrivateKey(privateKeyValue) 
    importResultData(returncode, stdout)
    return redirect(url_for('AccountDashBoard'))

@app.route('/uploaderPrivateKey', methods=['POST'])
def uploaderPrivateKeyInput():    
    uploaded_file = request.files['myKeyFile']
    returncode, stdout = imPri.uploadPrivateKey(uploaded_file) 
    importResultData(returncode, stdout)
    return redirect(url_for('AccountDashBoard'))
    
@app.route('/sendEther', methods=['POST'])
def selectRecipientInput():
    global _global_principal_address, _global_recipient_address    
    _global_recipient_address = request.form['recipient']    
    # print("Selected Recipient Data :", recipientAddress)       
    accountImageCreation(_global_recipient_address)        
    return render_template('ether_display.html', value0=_global_principal_address, value1=_global_recipient_address)

@app.route('/transferEther', methods=['POST'])        
def etherTransaction():        
    global _global_principal_address, _global_recipient_address        
    etherAmount = request.form['inputEtherValue']
    txResultData(sendWebEther(_global_recipient_address, _global_principal_address, etherAmount))           
    return redirect(url_for('AccountDashBoard'))

@app.route('/convertUSD', methods=['GET'])
def convertUSD():                    
    convertedValue = request.args.get('inputEtherValue') 
    try:             
        if "".__eq__(convertedValue):
            return jsonify({'result': 0})    
        else:
            return jsonify({'result': toTransUSD(convertedValue)})      
    except ValueError:
        return jsonify({'result': 0})    

@app.route('/progress')
def progress():
    def generate():
        x = 0
        while x < 100:            
            x = x + 10
            time.sleep(0.8)
            yield "data:" + str(x) + "\n\n"
    return Response(generate(), mimetype= 'text/event-stream')   

@app.route('/verifyKeyPhrase')
def verifyKeyPhrase():
    _principal_address_privateKey = extractPrincipalCipher(_global_principal_address)
    # print(extractPrincipalCipher(_global_principal_address))
    return render_template('input_keyphrase.html', value0=_global_principal_address, value1=_principal_address_privateKey)

@app.route('/MnemonicScalp', methods=['GET', 'POST'])
def MnemonicScalp():
    global Stop_Threads      
    form = PowerState()  
    thread_lists = []         

    if form.validate_on_submit():        
        if(form.state.label.text == 'OFF'):
            PowerState.state = SubmitField('ON')                              
            Stop_Threads = False            
            background_thread = Thread(name='MnemonicScalp', target=triggerMnemonicScalp, args=(lambda: Stop_Threads,))                                       
            background_thread.start() 
            thread_lists.append(background_thread)             
        elif(form.state.label.text == 'ON'):     
            PowerState.state = SubmitField('OFF')                                                   
            # Wait for all threads to complete
            Stop_Threads = True                         
            for thread in thread_lists:                                
                thread.join()                  

    return render_template('scalping.html', form=form)

@app.route('/streamData', methods=['GET'])
def streamData():
    def generate():
        with open(KEY_BASE+'/importedKey/importedPrivateKeys') as f:
            while True:
                yield f.read()                                
                sleep(1)           

    return app.response_class(generate(), mimetype='text/plain')        


# Development Debug Environment
if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5000)


# Production Environment
# if __name__ == "__main__":
#     from waitress import serve
#     serve(app, host="0.0.0.0", port=5000)