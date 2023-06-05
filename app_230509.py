# request フォームから送信した情報を扱うためのモジュール
# redirect  ページの移動
# url_for アドレス遷移
from flask import Flask, render_template, request, url_for, redirect
# 画像のダウンロード
from flask import send_from_directory
from werkzeug.utils import secure_filename

import os

DEBUG = True
SECRET_KEY = 'development key'
UPLOAD_FOLDER = './static/image'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.config.from_object(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=["GET"])
def show_index():
    return render_template("entrance.html")

@app.route('/', methods=["GET",'POST'])
def do_upload():
    file = request.files['xhr2upload']
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print("やっとここまできた")
        return redirect(url_for("uploaded_file", filename=filename))
    else :
        print("ここまできた")
        
@app.route('/upload',methods=["GET"])
# ファイルを表示する
def uploaded_file():
    return render_template("show_pdf.html")
 #   return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    

if __name__ == '__main__':
    app.run()