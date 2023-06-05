//#JSが読み込まれることの確認。
window.onload = function(){
    alert("Hello, JS.File is successfully loaded!!")
}

//fetch()のテスト前バージョンはdnd copy.js
let formData = new FormData();

const upload = () => {
  const btn = document.getElementById('submit_btn'); //送信ボタン
  file = document.getElementById('img_file'); //file
  btn.disabled = true; //連打防止
  btn.value="送信中";
  fetch('/api/pics', {
    method: 'POST',
    body: formData ,
  }).then(res => res.json()
  ).then(json => {
    if(json["status"] == "false"){ //Flask側で"false"と判断されたらアラートする
      alert(json["message"])
    }
    afterPost(); //POST後の処理
  })
};

const onSelectFile = () => upload();
document.getElementById('submit_btn').addEventListener('click', onSelectFile, false);

// ドラッグ&ドロップエリアの取得
var fileArea = document.getElementById('dropArea');

// input[type=file]の取得
var fileInput = document.getElementById('uploadFile');

// ドラッグオーバー時の処理
fileArea.addEventListener('dragover', function(e){
    e.stopPropagation();
    e.preventDefault();
    this.style.background = '#e1e7f0';
    fileArea.classList.add('dragover');
} , false);

// ドラッグアウト時の処理
fileArea.addEventListener('dragleave', function(e){
    e.stopPropagation();
    e.preventDefault();
    this.style.background = '#ffffff';
    fileArea.classList.remove('dragover');
} , false);

// ドロップ時の処理
fileArea.addEventListener('drop', function(e){
    e.stopPropagation();
    e.preventDefault();
    fileArea.classList.remove('dragover');

    // ドロップしたファイルの取得
    var files = e.dataTransfer.files;

    // 取得したファイルをinput[type=file]へ
    fileInput.files = files;
    
    if(typeof files[0] !== 'undefined') {
        //ファイルが正常に受け取れた際の処理
        window.addEventListener("load", () => {
            const input = document.getElementById('img_file');
            input.addEventListener("change", () => {
              formData.append('img_file', input.files[0]);
            });
          })
    } else {
        //ファイルが受け取れなかった際の処理
        alert("ふぁいるがありません");
    }
}, false);

// input[type=file]に変更があれば実行
// ドロップ以外でも発火
fileInput.addEventListener('change', function(e){
    e.stopPropagation();
    e.preventDefault();
    var file = e.target.files[0];
    //if (file) {
	//	getfileinfo(file);
	//}
    
    if(typeof e.target.files[0] !== 'undefined') {
        // ファイルが正常に受け取れた際の処理
        window.addEventListener("load", () => {
            const input = document.getElementById('img_file');
            input.addEventListener("change", () => {
              formData.append('img_file', input.files[0]);
            });
          })
        alert("2まできたよ");

    } else {
        //ファイルが受け取れなかった際の処理
        alert("ふぁいるがありません");
    }
}, false);