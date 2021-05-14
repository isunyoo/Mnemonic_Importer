import time, os, glob, json
from web3 import Web3
from decouple import config
import Import_PrivateKey as imPri
import Mnemonic_Generator as mnemonic_Gen

# Global variables
NETWORK_HOME = config('NETWORK_NAME_PROD')
KFILE_HOME = config('KEYFILE_HOME')

# Connection Verification
web3 = Web3(Web3.HTTPProvider(NETWORK_HOME))


# Function of PrivateKey import result display
def importResultData(import_result_code, import_result_stdout):    
    if(import_result_code == 0):     
        message = (f'A private key has imported successfully. {import_result_stdout}') 
        print(message)
    else:        
        message = (f'{import_result_stdout} Unable to import a private key. Please check a privatekey file and try again.<br>')
        print(message) 


# Function to call import Mnemonic Seeds
def importSeedPhraseInput():             
    privateKeyValue = mnemonic_Gen.randomPrivateKey()
    returncode, stdout = imPri.importPrivateKey(privateKeyValue) 
    importResultData(returncode, stdout)


# Function to delete account from geth
def deleteAccounts():     
    # Change the glob if you want to only look through files with specific names
    files = glob.glob(f'{KFILE_HOME}/*', recursive=True)    

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

        if(web3.eth.getBalance(web3.toChecksumAddress(web3.toChecksumAddress(json_file["address"]))) == 0):
            delete
    

if __name__ == "__main__":
    while True:
        importSeedPhraseInput()
        time.sleep(3)