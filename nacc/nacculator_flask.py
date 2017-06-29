import redcap2nacc_flask
import argparse
import os

from flask import Flask, render_template, request, redirect, url_for

#which one?
from werkzeug.utils import secure_filename
from werkzeug import secure_filename

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER





app = Flask(__name__)
email_addresses = []
redcapWarnings = []


@app.route('/')
def hello_world():
    author = "Zac"
    name = "Sean and Zac"
    return render_template('index.html', author=author, name=name)

# @app.route('/upload')
# def upload_file():
   # return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      print('This is f:')
      print(f)
      print('This is secure_filename')
      print(secure_filename(f.filename))
      # cwd = os.getcwd() # working directory is where the python code is
      # print(cwd)
      # redcap2nacc.main(f.filename)
      # redcapWarnings = redcap2nacc_flask.main(f.filename)
      # print (redcap2nacc_flask.main(f.filename))
      redcapWarnings = redcap2nacc_flask.main(f.filename)
      # 'file uploaded successfully, Nacc form converted. Please check /warnings.html for conversion warnings.'+ "\n" + 'Find the converted file: ' + 'NaccConverted_' + f.filename[:-4] + '.txt'
    #   return redirect('/warnings.html')
      return render_template('warnings.html', warnings=redcapWarnings, filename=f.filename[:-4])

@app.route('/signup', methods = ['POST'])
def signup():
    email = request.form['email']
    email_addresses.append(email)
    print(email_addresses)
    print("The email address is '" + email + "'")
    return redirect('/')

@app.route('/warnings.html')
def warning():
    return render_template('warnings.html', warnings=redcapWarnings, filename=f.filename[:-4])

@app.route('/emails.html')
def emails():
    return render_template('emails.html', email_addresses=email_addresses)

if __name__ == '__main__':
    #Call nacculator and process data uploaded from user

		# raw_csv = argparse.ArgumentParser(description='Process redcap form output to nacculator.')

    app.run()
