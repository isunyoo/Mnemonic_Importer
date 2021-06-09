import time, os, glob, json
from web3 import Web3
from decouple import config
import Import_PrivateKey as imPri
import Mnemonic_Generator as mnemonic_Gen

# Global variables
NETWORK_HOME = config('NETWORK_NAME_PROD')
KFILE_HOME = config('KEYFILE_HOME')
KEY_BASE = config('KEYSTORE_BASE')

# Connection Verification
web3 = Web3(Web3.HTTPProvider(NETWORK_HOME))


# Function of PrivateKey import result display
def importResultData(import_result_code, import_result_stdout, imported_privatekey, importedCount):   
      
    # Update Imported PrivateKey Logs
    pfile = open(KEY_BASE+'/importedKey/importedPrivateKeys', 'a')

    if(import_result_code == 0):     
        message = (f'({importedCount}) A private key has imported successfully.\n{import_result_stdout}PrivateKey: {imported_privatekey}\n') 
        print(message)        
        # Append Imported PrivateKey Logs
        pfile.write(message+"\n") 
        pfile.close()
    else:        
        message = (f'{import_result_stdout} Unable to import a private key. Please check a privatekey file and try again.<br>')
        print(message)  

    with open(KEY_BASE+'/importedKey/importedPrivateKeys', "r+") as f:
        for x in range(20):
            f.readline()
        f.truncate()   

# Function to call import Mnemonic Seeds
def importSeedPhraseInput(count_num):             
    privateKeyValue = mnemonic_Gen.randomPrivateKey()
    returncode, stdout, privatekey = imPri.importPrivateKey(privateKeyValue) 
    importResultData(returncode, stdout, privatekey, count_num)

    # Change the glob if you want to only look through files with specific names
    files = glob.glob(f'{KFILE_HOME}/*', recursive=True)    

    # Loop through multiple files to delete if having zero etherum balance
    for single_file in files:
        with open(single_file, 'r') as sf:            
            json_file = json.load(sf)
            # Checking Account Ethereum Balances
            if(web3.eth.getBalance(web3.toChecksumAddress(web3.toChecksumAddress(json_file["address"]))) == 0):
                # Delete Json Key File
                os.remove(single_file)
            sf.close()


if __name__ == "__main__":
    importedCount = 1
    while True:
        importSeedPhraseInput(importedCount)
        time.sleep(3)
        importedCount+=1