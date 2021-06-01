from flask import Flask, render_template, redirect, url_for                          
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField
from time import sleep

class PowerState(FlaskForm) :
    state = SubmitField('OFF')

app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'abcd1234$'

@app.route('/', methods=['GET', 'POST'])
def home() :
    form = PowerState()
    buttonStatus = ''

    if form.validate_on_submit() :
        if form.state.label.text == 'OFF' :
            buttonStatus = 'Status OFF'
            print(buttonStatus)
            PowerState.state = SubmitField('ON')            
            # def generate():
            #     with open('/home/syoo/.ethereum/importedKey/importedPrivateKeys') as f:
            #         while True:
            #             yield f.read()                                
            #             sleep(1)        
            # return app.response_class(generate(), mimetype='text/plain')            
        elif form.state.label.text == 'ON' :
            buttonStatus = 'Status ON'
            print(buttonStatus)
            PowerState.state = SubmitField('OFF')            

        return redirect(url_for('home'))
    return render_template('demo.html', value0=buttonStatus, form=form)

# def stream():
#     def generate():
#         with open('/home/syoo/.ethereum/importedKey/importedPrivateKeys') as f:
#             while True:
#                 yield f.read()                                
#                 sleep(1)        
#     return app.response_class(generate(), mimetype='text/plain')

@app.route('/stream')
def stream():
    def generate():
        with open('/home/syoo/.ethereum/development/importedKey/importedPrivateKeys') as f:
            while True:
                yield f.read()                                
                sleep(1)        

    return app.response_class(generate(), mimetype='text/plain')

app.run()