import os

import cv2
import numpy as np

#PDF>>peg等画像ファイルに変更#1個目TRY
from pathlib import Path
import pathlib
from pdf2image import convert_from_path
import glob
import img2pdf #pipにてインストール注意
from natsort import natsorted

#PDF>>peg等画像ファイルに変更#2個目TRY
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

import aspose.words as aw #pip経由注意

import csv #CSVファイル書き込み用


#PDF変換関数
def pdf_image(pdf_file,img_path, fmt='jpeg', dpi=200):

    #pdf_file、img_pathをPathにする
    pdf_path = Path(pdf_file)
    image_dir = Path(img_path)
    print('-2-')
    print(pdf_path)
    print(image_dir)
    # PDFをImage に変換(pdf2imageの関数)
    pages = convert_from_path(pdf_path, dpi)

    # 画像ファイルを１ページずつ保存
    for i, page in enumerate(pages):
        file_name = "{}_{:02d}.{}".format(pdf_path.stem,i+1,fmt)
        image_path = image_dir / file_name
        page.save(image_path, fmt)

# テキストを検出するクラス
class text_detector:
    # コンストラクタ
    def __init__(self):
        self._init_model()

    # モデルを準備する
    def _init_model(self):
        # モデルを読み込む
        directory = os.path.dirname(__file__)
        print(directory)
        # weights = os.path.join(directory, "DB_TD500_resnet50.onnx")  # 英語, 中国語, 数字
        # weights = os.path.join(directory, "DB_TD500_resnet18.onnx")  # 英語, 中国語, 数字
        weights = os.path.join(directory, "DB_IC15_resnet50.onnx")     # 英語, 数字
        # weights = os.path.join(directory, "DB_IC15_resnet18.onnx")   # 英語, 数字
        self._model = cv2.dnn_TextDetectionModel_DB(weights)

        # モデルの推論に使用するエンジンとデバイスを設定する
        self._model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self._model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        # モデルの入力パラメーターを設定する
        scale = 1.0 / 255.0                                # スケールファクター
        # size = (736, 736)                                # 入力サイズ（MSRA-TD500）
        size = (736, 1280)                                 # 入力サイズ（ICDAR2015）
        mean = (122.67891434, 116.66876762, 104.00698793)  # 差し引かれる平均値
        swap = False                                       # チャンネルの順番（True: RGB、False: BGR）
        crop = False                                       # クロップ
        self._model.setInputParams(scale, size, mean, swap, crop)

        # テキスト検出のパラメーターを設定する
        binary_threshold = 0.3   # 二値化の閾値
        polygon_threshold = 0.5  # テキスト輪郭スコアの閾値
        max_candidates = 200     # テキスト候補領域の上限値
        unclip_ratio = 2.0       # アンクリップ率
        self._model.setBinaryThreshold(binary_threshold)
        self._model.setPolygonThreshold(polygon_threshold)
        self._model.setMaxCandidates(max_candidates)
        self._model.setUnclipRatio(unclip_ratio)

    # 画像からテキストを検出する（座標）
    def detect_vertices(self, image):
        if self._model is None:
            raise IOError("failed model has not been created!")

        if image is None:
            raise IOError("failed image is empty!")

        # テキストを検出する（座標）
        vertices, confidences = self._model.detect(image)

        return vertices, confidences

    # 画像からテキストを検出する（中心座標、領域サイズ、回転角度）
    def detect_rotated_rectangles(self, image):
        if self._model is None:
            raise IOError("failed model has not been created!")

        if image is None:
            raise IOError("failed image is empty!")

        # テキストを検出する（中心座標、領域サイズ、回転角度）
        rotated_rectangles, confidences = self._model.detectTextRectangles(image)

        return rotated_rectangles, confidences

# テキストを認識するクラス
class text_recognizer:
    # コンストラクタ
    def __init__(self):
        self._init_model()

    # モデルを準備する
    def _init_model(self):
        # モデルを読み込む
        directory = os.path.dirname(__file__)
        # weights = os.path.join(directory, "crnn.onnx")        # 英語, 数字
        weights = os.path.join(directory, "crnn_cs.onnx")       # 英語, 数字, 記号
        # weights = os.path.join(directory, "crnn_cs_CN.onnx")  # 英語, 中国語, 数字, 記号
        self._model = cv2.dnn_TextRecognitionModel(weights)

        # モデルの推論に使用するエンジンとデバイスを設定する
        self._model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self._model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        # グレースケール画像を要求する（CRNNのみ）
        self._require_gray = False
        if "crnn.onnx" in weights:
            self._require_gray = True

        # モデルの入力パラメーターを設定する
        scale = 1.0 / 127.5           # スケールファクター
        size = (100, 32)              # 入力サイズ
        mean = (127.5, 127.5, 127.5)  # 差し引かれる平均値
        swap = True                   # チャンネルの順番（True: RGB、False: BGR）
        crop = False                  # クロップ
        self._model.setInputParams(scale, size, mean, swap, crop)

        # デコードタイプを設定する
        type = "CTC-greedy"               # 貪欲法
        # type = "CTC-prefix-beam-search" # ビーム探索
        self._model.setDecodeType(type)

        # 語彙リストを設定する
        # vocabulary_file = os.path.join(directory, "alphabet_36.txt")    # 英語, 数字
        vocabulary_file = os.path.join(directory, "alphabet_94.txt")      # 英語, 数字, 記号
        # vocabulary_file = os.path.join(directory, "alphabet_3944.txt")  # 英語, 中国語, 数字, 記号
        vocabularies = self._read_vocabularies(vocabulary_file)
        self._model.setVocabulary(vocabularies)

    # ファイルから語彙リストを読み込む
    def _read_vocabularies(self, file):
        vocabularies = None
        with open(file, mode='r', encoding="utf-8") as f:
            vocabularies = f.read().splitlines()
        return vocabularies

    # 画像からテキストを認識する
    def recognize(self, image):
        if self._model is None:
            raise IOError("failed model has not been created!")

        if image is None:
            raise IOError("failed image is empty!")

        # グレースケール画像に変換する
        channels = 1 if len(image.shape) == 2 else image.shape[2]
        if self._require_gray and channels != 1:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # テキストを認識する
        text = self._model.recognize(image)
        return text

# 画像とテキスト領域の座標リストからテキスト領域の画像を切り出す関数
def get_text_images(image, vertices):
    text_images = []
    size = (100, 32)
    for vertex in vertices:
        source_poins = np.array(vertex, dtype=np.float32)
        target_poins = np.array([[0, size[1]], [0, 0], [size[0], 0], [size[0], size[1]]], dtype=np.float32)
        transform_matrix = cv2.getPerspectiveTransform(source_poins, target_poins)
        text_image = cv2.warpPerspective(image, transform_matrix, size)
        text_images.append(text_image)
    return text_images


# 回転矩形から矩形四隅の頂点座標（左下から時計回り）を取得する
def get_vertices(rotated_rectangles):
    vertices = []
    for rotated_rectangle in rotated_rectangles:
        points = cv2.boxPoints(rotated_rectangle)
        bl = tuple(map(int, points[0]))  # 左下
        tl = tuple(map(int, points[1]))  # 左上
        tr = tuple(map(int, points[2]))  # 右上
        br = tuple(map(int, points[3]))  # 右下
        vertices.append([bl, tl, tr, br])
    return vertices




def main(filename):
    # キャプチャを開く
    directory = os.path.dirname(__file__)
    file = os.path.join(directory, "static" , "image" , filename)

    pdf_path = Path(file)
    img_path = Path(os.path.join(directory, "static",  "image"))
    fmt='jpeg'
    pdf_image(pdf_file=pdf_path,img_path=img_path, fmt='jpeg', dpi=200)
    
    file_name = "{}_{:02d}.{}".format(pdf_path.stem, 1 ,fmt)
    #file_path = Path(os.path.join(directory, "static" , "image", file_name))

    #print('-1-')
    #print(file_path)
    #file_path = os.path.join(directory, "static\\image" , file_name)
    
    capture = cv2.VideoCapture(os.path.join(directory, "static" , "image", file_name))  # 画像ファイル 
    #capture = cv2.imread(file)  # 画像ファイル <<filenameに変更230513
    #capture = cv2.rotate(file, cv2.ROTATE_90_CLOCKWISE)

    # capture = cv2.VideoCapture(0)  # カメラ
    if not capture.isOpened():
       raise IOError("can't open capture!")

    # テキスト検出器の生成
    detector = text_detector()

    # テキスト認識器の生成
    recognizer = text_recognizer()

    while True:
        # フレームをキャプチャして画像を読み込む
        result, image_org = capture.read()
        image = image_org
        #image = cv2.rotate(image_org, cv2.ROTATE_90_CLOCKWISE) #90度回転の場合
        if result is False:
            cv2.waitKey(0)
            break

        # 画像が3チャンネル以外の場合は3チャンネルに変換する
        channels = 1 if len(image.shape) == 2 else image.shape[2]
        if channels == 1:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        if channels == 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

        # テキスト検出（座標）
        vertices, _ = detector.detect_vertices(image)

        # テキスト領域の画像を切り出す
        text_images = get_text_images(image, vertices)

        # テキスト検出（中心座標、領域サイズ、回転角度）
        # rotated_rectangles, _ = detector.detect_rotated_rectangles(image)
        # vertices = get_vertices(rotated_rectangles)  # テキスト検出（座標）と同じ

        # テキストを認識する
        texts = []
        list_out = []
        list1 = [] 
        n = 1
        for text_image in text_images:
            text = recognizer.recognize(text_image)
            list1.append(n)
            list1.append(text)
            list_out.append(list1)
            list1 = []
            n += 1
            texts.append(text)

            
        
        # 検出したテキスト領域の矩形を描画する
        for vertex in vertices:
            vertex = np.array(vertex)
            close = True
            color = (0, 255, 0)
            thickness = 2
            cv2.polylines(image, [vertex], close, color, thickness, cv2.LINE_AA)
        
        # テキスト認識の結果を描画する
        i = 1

        for text, vertex in zip(texts, vertices):
            position = vertex[1] - (0, 10)
            font = cv2.FONT_HERSHEY_SIMPLEX
            scale = 0.7
            color = (0, 0, 255)
            cv2.putText(image, "{}".format(i), position, font, scale, color, thickness, cv2.LINE_AA)
            i += 1
        
        # 画像を表示する>>ここを保存に変える
        #cv2.imshow("text detection", image)
        #key = cv2.waitKey(10)
        #if key == ord('q'):
            #break

    #cv2.destroyAllWindows()
        file_out_path = Path(file_name)
        file_out = "{}_{}.{}".format(file_out_path.stem, "out" ,fmt)
        file_out_dm = os.path.join(directory, "static" , "image_out", file_out) 
        cv2.imwrite(file_out_dm , image)  # 画像を保存する JPEG形式

        print(texts)
        with open(os.path.join(directory, "static" , "image_out", "C_file_out.csv") , 'w') as f:
            writer = csv.writer(f)
            writer.writerows(list_out)

    # 新しいドキュメントを作成する
        doc = aw.Document()

    # ドキュメント ビルダーを作成する
        builder = aw.DocumentBuilder(doc)

    # ドキュメントに画像を挿入する
        builder.insert_image(file_out_dm)

    # PDFとして保存
        outputpath = os.path.join(directory, "static" , "image_out", "file.pdf")
        doc.save(outputpath)

        # 画像をファイルから読み込む
        #image = Image.open(file_out_dm)
        # 画像をNumpy配列に変換する
        #image = np.asarray(image)

        # 画像のプロット先の準備
        #fig = plt.figure()
        # グリッドの表示をOFFにする
        #plt.axis('off')
        # Numpy配列を画像として表示する
        #plt.imshow(image)

        # 保存するPDFファイル名
        #outputpath = os.path.join(directory, "static" , "image_out", "file.pdf")
        #pp = PdfPages(outputpath)
        # 画像をPDFとして保存する
        #pp.savefig(fig)
        # PDFの保存終了
        #pp.close()
        
        lists = []
        lists = list(glob.glob("*\\image_out\\*.jpeg"))
        outputpath = os.path.join(directory, "static" , "image_out", "file.pdf") 
        with open(outputpath,"wb") as f:
            f.write(img2pdf.convert([str(i) for i in natsorted(lists) if ".jpeg" in i]))

if __name__ == '__main__':
    main()

