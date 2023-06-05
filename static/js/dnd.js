//#JSが読み込まれることの確認。
//window.onload = function(){
    //alert("Hello, JS.File is successfully loaded!!")
//} ;

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

function anaFile(file) {  
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

function previewFile(file) {
    //const pdfInput = document.getElementById('pdf-input');
    var pdfContainer = document.getElementById('dropArea');
    var fileInput = document.getElementById('targetfileid');  // add by kido 0509

    //pdfInput.addEventListener('change', () => {
            //const file = pdfInput.files[0];
            //if (file.type === 'application/pdf') {
                var reader = new FileReader();
                reader.onload = () => {
                    var pdfData = reader.result;
                    pdfContainer.innerHTML = `<embed src="${pdfData}#navpanes=0" type="application/pdf" width="100%" height="100%" />`;
                    // vvvv add by kido 0509 vvvv
                    const dt = new DataTransfer();
                    dt.items.add(file);
                    fileInput.files = dt.files;
                    // ^^^^ add by kido 0509 ^^^^
                };
                reader.readAsDataURL(file);
            //} else {
                //alert('PDFファイルを選択してください。');
            //}
        //});
    };

// ドラッグ&ドロップエリアの取得
var fileArea = document.getElementById('dropArea');

// input[type=file]の取得 
var fileInput = document.getElementById('previewFile');

// input[type=file]の取得 
//var fileInput = document.getElementById('uploadFile');

// 解析開始ボタン：input[type=file]の橋渡し
var fileSend = document.getElementById('uploadFile');

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
        previewFile(files[0]);
       // alert("1まできたよ");
        
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
        previewFile(file_02);
       // alert("2まできたよ");
        

    } else {
        // ファイルが受け取れなかった際の処理
        alert("ふぁいるがありません");
    }
}, false);


//解析用のボタンを押したときの操作
// input[type=file]に変更があれば実行
// もちろんドロップ以外でも発火します。解析開始フラグ用、サーバーにfile送信し解析開始
fileSend.addEventListener('click', function(e){
    document.getElementById("uploadform").submit();
    //e.stopPropagation();
    //e.preventDefault();
    //var file_03 = e.currentTarget.files[0];
    //if (file) {
	//	getfileinfo(file);
	//}
    /*
    if(typeof e.target.files[0] !== 'undefined') {
        // ファイルが正常に受け取れた際の処理
        uploadFile(file_03);
        alert("3まできたよ");

    } else {
        // ファイルが受け取れなかった際の処理
        alert("ふぁいるがありません");
    }*/
}, false);

