# The basic structure is from http://opentechschool.github.io/python-flask/core/setup.html
import redcap2nacc_flask
import argparse
import os
from flask import Flask, render_template, request, redirect, url_for, \
send_from_directory #, Response

# Referrence https://n8henrie.com/2015/05/better-bootstrap-file-upload-button/
#from forms import UploadForm
# To operate the uploaded file
from werkzeug.utils import secure_filename
from werkzeug import secure_filename


# from http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
email_addresses = []
redcapWarnings = []

# Main Page
@app.route('/')
def hello_world():
    author = "Zac"
    name = "Sean and Zac"
    return render_template('index.html', author=author, name=name)

# @app.route('/upload')
# def upload_file():
   # return render_template('upload.html')

##### The upload and download part is somewhat tricky.
# Resources:
# http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
# https://stackoverflow.com/questions/24577349/flask-download-a-file
# Additional resource that might be helpful
# https://stackoverflow.com/questions/27628053/uploading-and-downloading-files-with-flask

# The upload action/button
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      file = request.files['file']
      if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
      if file:
          somefilename = secure_filename(file.filename)
          file.save(secure_filename(file.filename))
          file.save(os.path.join(app.config['UPLOAD_FOLDER'], somefilename))
      redcapWarnings = redcap2nacc_flask.main(file.filename)
      # 'file uploaded successfully, Nacc form converted. Please check /warnings.html for conversion warnings.'+ "\n" + 'Find the converted file: ' + 'NaccConverted_' + file.filename[:-4] + '.txt'
    #   return redirect('/warnings.html')
      return render_template('warnings.html', warnings=redcapWarnings, \
      filename=file.filename[:-4], downloadname='NaccConverted_' + \
      file.filename[:-4] + '.txt')

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    # uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    uploads = app.root_path
    return send_from_directory(directory=uploads, filename=filename)

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)

@app.route('/signup', methods = ['POST'])
def signup():
    email = request.form['email']
    email_addresses.append(email)
    print(email_addresses)
    print("The email address is '" + email + "'")
    return redirect('/')

@app.route('/warnings.html')
def warning():

    return render_template('warnings.html', warnings=redcapWarnings, \
    filename=file.filename[:-4])


@app.route('/emails.html')
def emails():
    return render_template('emails.html', email_addresses=email_addresses)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

if __name__ == '__main__':
    #Call nacculator and process data uploaded from user
    # raw_csv = argparse.ArgumentParser(description='Process redcap form output to nacculator.')
    app.run(host='0.0.0.0')
