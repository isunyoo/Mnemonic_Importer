from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField
from decouple import config
from time import sleep


# Global variables
KEY_BASE = config('KEYSTORE_BASE')

class PowerState(FlaskForm) :
    state = SubmitField('ON')

app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'abcd1234$'

@app.route('/', methods=['GET', 'POST'])
def home() :
    form = PowerState()
    buttonStatus = False    

    if form.validate_on_submit() :
        if form.state.label.text == 'OFF' :
            buttonStatus = True
            PowerState.state = SubmitField('ON')                        
        elif form.state.label.text == 'ON' :
            buttonStatus = False                                               
            PowerState.state = SubmitField('OFF')            
        
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