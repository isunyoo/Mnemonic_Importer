from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField
from decouple import config
from time import sleep
import Mnemonic_Scalping as mnemonic_Scalp

# Global variables
KEY_BASE = config('KEYSTORE_BASE')

# Function to trigger Mnemonic Scalping Process
def triggerMnemonicScalp(buttonStatus):
    importedCount = 1    
    while True:                   
        if(buttonStatus == True):                  
            # mnemonic_Scalp.importSeedPhraseInput(importedCount)                
            # sleep(3)
            # importedCount+=1
            print(buttonStatus)
        elif(buttonStatus == False):                     
            print(buttonStatus)
            break
            # exit()
        
class PowerState(FlaskForm):
    state = SubmitField('ON')

# Flask http web display
app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'abcd1234$'

@app.route('/', methods=['GET', 'POST'])
def home():
    form = PowerState()
    buttonStatus = False
    triggerMnemonicScalp(buttonStatus) 

    if form.validate_on_submit():
        if(form.state.label.text == 'OFF'):
            PowerState.state = SubmitField('ON')
            buttonStatus = True            
            # triggerMnemonicScalp(buttonStatus)                                                
        elif(form.state.label.text == 'ON'):     
            PowerState.state = SubmitField('OFF')    
            buttonStatus = False                                
            # triggerMnemonicScalp(buttonStatus)                                                        
        
    return render_template('index.html', value0=buttonStatus, form=form)
    

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