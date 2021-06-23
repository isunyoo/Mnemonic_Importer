import time, binascii
from mnemonic import Mnemonic
import Mnemonic_util as imMnemonic

mnemo = Mnemonic("english")

def randomPrivateKey(): 
    seedPhraseValue = mnemo.generate(strength=128)    
    biPrivateKey = imMnemonic.mnemonic_to_private_key(seedPhraseValue)    
    strPrivateKey = format(str(binascii.hexlify(biPrivateKey), 'utf-8'))
    return strPrivateKey

# while True:
#     # seedPhraseValue = mnemo.generate(strength=256)
#     seedPhraseValue = mnemo.generate(strength=128)    
#     print(seedPhraseValue)    

#     biPrivateKey = imMnemonic.mnemonic_to_private_key(seedPhraseValue)    
#     print("Your private key is: {}".format(str(binascii.hexlify(biPrivateKey), 'utf-8')))

#     seed = mnemo.to_seed(seedPhraseValue, passphrase="")
#     print("Your Seed key is: {}".format(str(binascii.hexlify(seed), 'utf-8')))

#     entropy = mnemo.to_entropy(seedPhraseValue)
#     print("Your Entropy key is: {}".format(str(binascii.hexlify(entropy), 'utf-8')))
    
#     time.sleep(3)
