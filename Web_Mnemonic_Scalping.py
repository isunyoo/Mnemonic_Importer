from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField
from time import sleep
from decouple import config
from threading import Thread
import Mnemonic_Scalping as mnemonic_Scalp

# Global variables
KEY_BASE = config('KEYSTORE_BASE')
Stop_Threads = False

# Function to trigger Mnemonic Scalping Process
def triggerMnemonicScalp(stop_status):
    importedCount = 1    
    # while True:                   
    #     if(buttonStatus == True):                  
    #         # mnemonic_Scalp.importSeedPhraseInput(importedCount)                
    #         # sleep(3)
    #         # importedCount+=1
    #         print(buttonStatus)
    #     elif(buttonStatus == False):                     
    #         print(buttonStatus)
    #         break
    #         # exit()
    while True:
        global Stop_Threads                
        mnemonic_Scalp.importSeedPhraseInput(importedCount)                
        sleep(3)
        importedCount+=1        
        if stop_status():
            break

# def threadController(buttonStatus):
#     global Stop_Threads

#     background_thread = Thread(target=triggerMnemonicScalp, args=(lambda: Stop_Threads,))               
#     if(buttonStatus == False): 
#         Stop_Threads = False        
#         background_thread.start()    
#     elif(buttonStatus == True):                         
#         Stop_Threads = True
#         background_thread.join()


class PowerState(FlaskForm):
    state = SubmitField('ON')

# Flask http web display
app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'abcd1234$'

@app.route('/', methods=['GET', 'POST'])
def home():
    form = PowerState()
    # global Stop_Threads 
    buttonStatus = False    

    if form.validate_on_submit():        
        if(form.state.label.text == 'OFF'):
            PowerState.state = SubmitField('ON')
            buttonStatus = True                          
            Stop_Threads = False
            background_thread = Thread(target=triggerMnemonicScalp, args=(lambda: Stop_Threads,))                 
            background_thread.start()      
            # background_thread = Thread(target=triggerMnemonicScalp)        
            # triggerMnemonicScalp(buttonStatus)   
        elif(form.state.label.text == 'ON'):     
            PowerState.state = SubmitField('OFF')    
            buttonStatus = False                              
            background_thread = Thread(target=triggerMnemonicScalp, args=(lambda: Stop_Threads,))         
            background_thread.start()    
            sleep(1)
            Stop_Threads = True        
            background_thread.join()                
            # background_thread = Thread(target=triggerMnemonicScalp)                       
            # triggerMnemonicScalp(buttonStatus)                                                        
        
    return render_template('index.html', value0=buttonStatus, form=form)
    
# https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/

@app.route('/streamData', methods=['GET'])
def streamData():
    def generate():
        with open(KEY_BASE+'/importedKey/importedPrivateKeys') as f:
            while True:
                yield f.read()                                
                sleep(1)        

    return app.response_class(generate(), mimetype='text/plain')        


if __name__ == '__main__':                                                                                                                                                                     
    app.debug = True                                                                                                                                                                           
    app.run()