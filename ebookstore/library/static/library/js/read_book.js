pdfjsLib.GlobalWorkerOptions.workerSrc =
"https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.worker.min.js";

const pdfData = document.querySelector('#pdfData');
const url = pdfData?.dataset.url;
let pageNum = parseInt(pdfData?.dataset.page) || 1;

let pdfDoc = null;

const canvas = document.querySelector('#pdfCanvas');
const ctx = canvas.getContext('2d');

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

function loadPDF(pdfUrl) {

    const loadingTask = pdfjsLib.getDocument({
        url: pdfUrl,
        withCredentials: false,
        cMapUrl: 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/cmaps/',
        cMapPacked: true
    });

    loadingTask.promise.then(pdf => {

        pdfDoc = pdf;
        renderPage(pageNum);

    }).catch(err => {
        console.error("PDF LOAD ERROR:", err);
    });
}

loadPDF(url);