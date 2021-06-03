<<<<<<< HEAD
from flask import Flask, render_template, redirect, url_for, stream_with_context, Response
=======
from flask import Flask, render_template, redirect, url_for, stream_with_context                       
>>>>>>> 7bdfa4378cd9630d96b6c19b12810a9d92a762eb
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
    buttonStatus = False
<<<<<<< HEAD
    streamDaata = ''
=======
    streamData = ''
>>>>>>> 7bdfa4378cd9630d96b6c19b12810a9d92a762eb

    if form.validate_on_submit() :
        if form.state.label.text == 'OFF' :
            buttonStatus = False
            buttonStatus = stream()
            print(buttonStatus)
            PowerState.state = SubmitField('ON')            
            # def generate():
            #     with open('/home/syoo/.ethereum/importedKey/importedPrivateKeys') as f:
            #         while True:
            #             yield f.read()                                
            #             sleep(1)        
            # return app.response_class(generate(), mimetype='text/plain')                              
        elif form.state.label.text == 'ON' :
            buttonStatus = True
            streamDaata = stream()  
            print(buttonStatus)                                    
            PowerState.state = SubmitField('OFF')            

        # return redirect(url_for('home'))
<<<<<<< HEAD
    return render_template('demo.html', value0=buttonStatus, value1=streamDaata, form=form)

def stream():
    def generate():
        with open('/home/syoo/.ethereum/development/importedKey/importedPrivateKeys') as f:
            while True:
                yield f.read()                                
                sleep(1)        
    # return app.response_class(generate(), mimetype='text/plain')    
    return Response(stream_with_context(generate()))
=======
    return render_template('demo.html', value0=buttonStatus, value1=streamData, form=form)

def stream():
    def generate():
        with open('/home/syoo/.ethereum/importedKey/importedPrivateKeys') as f:
            while True:
                yield f.read()                                
                sleep(1)        
    # return app.response_class(generate(), mimetype='text/plain')
    return app.response_class(stream_with_context(generate()))

>>>>>>> 7bdfa4378cd9630d96b6c19b12810a9d92a762eb

@app.route('/stream')
def stream():
    def generate():
        with open('/home/syoo/.ethereum/development/importedKey/importedPrivateKeys') as f:
            while True:
                yield f.read()                                
                sleep(1)        

    # return app.response_class(generate(), mimetype='text/plain')
    return Response(stream_with_context(generate()))

app.run()