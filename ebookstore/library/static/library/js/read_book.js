pdfjsLib.GlobalWorkerOptions.workerSrc =
"https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.worker.min.js";

const dataEl = document.querySelector('#pdfData');
const url = dataEl?.dataset.url;

const canvas = document.querySelector('#pdfCanvas');
const ctx = canvas?.getContext('2d');

let pdfDoc = null;
let pageNum = parseInt(dataEl?.dataset.page || 1);

/* STOP IF NO URL */
if (!url || url === "None" || url.trim() === "") {
    console.error("PDF URL missing or invalid:", url);
    document.querySelector("#reader").innerHTML =
        "<h5 class='text-danger text-center'>PDF not available</h5>";
} else {

    pdfjsLib.getDocument(url).promise
        .then(pdf => {
            pdfDoc = pdf;
            renderPage(pageNum);
        })
        .catch(err => {
            console.error("PDF load failed:", err);
            document.querySelector("#reader").innerHTML =
                "<h5 class='text-danger text-center'>Failed to load PDF</h5>";
        });

}


function renderPage(num) {
    pdfDoc.getPage(num).then(page => {

        const viewport = page.getViewport({ scale: 1.5 });

        canvas.height = viewport.height;
        canvas.width = viewport.width;

        page.render({
            canvasContext: ctx,
            viewport: viewport
        });

    }).catch(err => {
        console.error("Page render error:", err);
    });
}