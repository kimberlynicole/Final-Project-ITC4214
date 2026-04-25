/*
========================================================
PDF READER (WORKING CLEAN VERSION)
========================================================
*/

pdfjsLib.GlobalWorkerOptions.workerSrc =
"https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.worker.min.js";

const url = document.querySelector('#pdfData')?.dataset.url;
const initialPage = document.querySelector('#pdfData')?.dataset.page;

let pdfDoc = null;
let pageNum = parseInt(initialPage) || 1;

const canvas = document.querySelector('#pdfCanvas');
const ctx = canvas.getContext('2d');

const pageNumEl = document.querySelector('#page-num');
const pageCountEl = document.querySelector('#page-count');

/* RENDER PAGE */
function renderPage(num) {

    pdfDoc.getPage(num).then(page => {

        const viewport = page.getViewport({ scale: 1.5 });

        canvas.height = viewport.height;
        canvas.width = viewport.width;

        page.render({
            canvasContext: ctx,
            viewport: viewport
        });

    });
}

pdfjsLib.getDocument({
    url: url,
    withCredentials: false
}).promise.then(pdf => {

    pdfDoc = pdf;
    renderPage(pageNum);

}).catch(err => {
    console.error("PDF LOAD ERROR:", err);
});

