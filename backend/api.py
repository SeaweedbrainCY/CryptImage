from flask import Flask
from flask import request
from flask import redirect
import os
from flask import send_file
app = Flask(__name__)

@app.route("/")
def main():
    return "<p>Use this api to sign or verify an image</p>"


@app.route("/sign", methods=['GET', 'POST'])
def sign():
    import os
    print(os.getcwd())
    if request.method == 'POST':
        try :
            password = request.form['password']
        except  :
            return "Error. Impossible to retrieve the password."

        try :
            f = request.files['image']
            f.save('/var/www/html/image.png')
        except :
            return "Error. Impossible to retrieve the image."
        rep = os.popen("cd /home/admin/CryptImage; export PYTHONPATH=/home/admin/CryptImage; bin/./run.sh 1  /var/www/html/image.png " + password ).read()
        print(rep)
        if 'FAIL' in rep or "FATAL" in rep or "ERROR" in rep or "error" in rep or "fail" in rep or "FORBID" in rep or "forbid" in rep :
            return redirect("http://cryptimage.h.minet.net/forbidden.html", code=302)
        elif "SUCCESS" in rep or "success" in rep:
            try :
                return send_file('/var/www/html/image_signed.png', attachment_filename="image_signed.png")
            except:
                return "<p> Your image has been protected but impossible to send it. Please download it <a href='http://cryptimage.h.minet.net/image_protected.png'>here</a></p>"
        else :
            return redirect("http://cryptimage.h.minet.net/forbidden.html", code=302)
    else :
        return "<p>Please use POST request</p>"
