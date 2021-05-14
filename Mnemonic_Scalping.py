import time
from web3 import Web3
from decouple import config
import Import_PrivateKey as imPri
import Mnemonic_Generator as mnemonic_Gen

# Global variables
NETWORK_HOME = config('NETWORK_NAME_PROD')

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

def importSeedPhraseInput():             
    privateKeyValue = mnemonic_Gen.randomPrivateKey()
    returncode, stdout = imPri.importPrivateKey(privateKeyValue) 
    importResultData(returncode, stdout)


if __name__ == "__main__":
    while True:
        importSeedPhraseInput()
        time.sleep(3)