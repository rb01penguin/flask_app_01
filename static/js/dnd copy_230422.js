//#JSが読み込まれることの確認。
window.onload = function(){
    alert("Hello, JS.File is successfully loaded!!")
} ;

function uploadFile(file) {
    var upload_uri = "/";
    var xhr = new XMLHttpRequest();
    var fd = new FormData();
    var p_element = document.getElementById("text_message");
    
    xhr.open("post", upload_uri, true);
    //xhr.setRequestHeader('content-type', 'multipart/form-data');
    xhr.onreadystatechange = function() {
      if( xhr.readyState === 4 && xhr.status === 200) {
        console.log( xhr.responseText );
      }
    };
    fd.append('xhr2upload', file);
    xhr.send(fd);
} ;   

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
    //e.stopPropagation();
    e.preventDefault();
    fileArea.classList.remove('dragover');

    // ドロップしたファイルの取得
    var files = e.dataTransfer.files;

    // 取得したファイルをinput[type=file]へ
    fileInput.files = files;
    
    if(typeof files[0] !== 'undefined') {
        //ファイルが正常に受け取れた際の処理
        uploadFile(files[0]);
        alert("1まできたよ");
    } else {
        //ファイルが受け取れなかった際の処理
        alert("ふぁいるがありません");
    }
}, false);

// input[type=file]に変更があれば実行
// もちろんドロップ以外でも発火します
fileInput.addEventListener('change', function(e){
    //e.stopPropagation();
    //e.preventDefault();
    var file_02 = e.target.files[0];
    //if (file) {
	//	getfileinfo(file);
	//}
    
    if(typeof e.target.files[0] !== 'undefined') {
        // ファイルが正常に受け取れた際の処理
        uploadFile(file_02);
        alert("2まできたよ");

    } else {
        // ファイルが受け取れなかった際の処理
        alert("ふぁいるがありません");
    }
}, false);