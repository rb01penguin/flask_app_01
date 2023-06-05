// 解析開始ボタン：input[type=file]の橋渡し
var fileSend = document.getElementById('downloadFile');

fileSend.addEventListener('click', function(e){
    document.getElementById("downloadFile").submit();
    
}, false);



