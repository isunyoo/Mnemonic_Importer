from time import sleep
from decouple import config
from threading import Thread
from flask import Flask, render_template, redirect, url_for  
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField
import Mnemonic_Scalping as mnemonic_Scalp

# Global variables
KEY_BASE = config('KEYSTORE_BASE')
Stop_Threads = False

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

class PowerState(FlaskForm):
    state = SubmitField('ON')

# Flask http web display
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
Bootstrap(app)

app.config['SECRET_KEY'] = 'abcd1234$'

@app.route('/', methods=['GET', 'POST'])
def home():
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

        # return redirect(url_for('home'))                    
    return render_template('index.html', form=form)

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