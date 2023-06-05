//ここにPDFのURL
var url = "/static/image/y1-1.pdf";
 
var pdfjsLib = window['pdfjs-dist/build/pdf'];

// pdf.worker.js のURL
pdfjsLib.GlobalWorkerOptions.workerSrc = "/static/pdfjs-dist/build/pdf.worker.js";

var loadingTask = pdfjsLib.getDocument(url);
var pdfjs_target = document.getElementById('pdfjs_view');
 
var page_w = 1000;
var scale = 1;

loadingTask.promise.then(
    function (pdf) {
        for( var i=1; i<=pdf._pdfInfo.numPages; i++ ){

            pdf.getPage(i).then(function (page) {
                 
                //横幅を1000pxに調整
                page_w = page._pageInfo.view[2];
                scale = 1000 / page_w;
                 

                var viewport = page.getViewport({ scale: scale });
                var canvas = document.createElement("canvas");
                var context = canvas.getContext("2d");
                canvas.width = viewport.width;
                canvas.height = viewport.height;

                var renderContext = {
                    canvasContext: context,
                    viewport: viewport,
                };
                pdfjs_target.appendChild(canvas);
                page.render(renderContext);
            });
        }
    }
);