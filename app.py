# request フォームから送信した情報を扱うためのモジュール
# redirect  ページの移動
# url_for アドレス遷移
from flask import Flask, render_template, request, url_for, redirect
# 画像のダウンロード
from flask import send_from_directory, send_file, make_response
from werkzeug.utils import secure_filename

import OCR_test_book01

import os
import shutil

DEBUG = True
SECRET_KEY = 'development key'
UPLOAD_FOLDER = './static/image'
OUT_FOLDER = './static/image_out'
ALLOWED_EXTENSIONS = set(['pdf']) #PDFのみのUPLOAD


app = Flask(__name__)
app.config.from_object(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=["GET"])
def show_index():
    target_dir1 = UPLOAD_FOLDER
    shutil.rmtree(target_dir1)
    os.mkdir(target_dir1)

    target_dir2 = OUT_FOLDER
    shutil.rmtree(target_dir2)
    os.mkdir(target_dir2)

    return render_template("entrance.html")

@app.route('/upload', methods=['POST'])
def do_upload():
    file = request.files['targetfile']
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print("やっとここまできた")

        OCR_test_book01.main(filename)

        return redirect(url_for("uploaded_file", filename="file.pdf"))
    else :
        print("ここまできた")
        
@app.route('/upload',methods=["GET"])
# ファイルを表示する
def uploaded_file():
    return render_template("show_pdf.html")
 #   return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download',methods=["POST","GET"])

def downloaded_file():
    return send_from_directory(app.config['OUT_FOLDER'], "C_file_out.csv", as_attachment = True )#, render_template("entrance.html") 

    

if __name__ == '__main__':
    app.run()