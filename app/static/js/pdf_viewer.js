/* * ZEN PDF EDITOR ENGINE
 * Handles: PDF.js rendering, Fabric.js canvas manipulation, and Page Management.
 */

document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Only run this if we are on the Editor Page
    const canvasElement = document.getElementById('pdfCanvas');
    if (!canvasElement) return; // Stop if no canvas found

    // --- CONFIGURATION ---
    const canvas = new fabric.Canvas('pdfCanvas', {
        backgroundColor: "#ffffff",
        selection: true
    });

    const pdfInput = document.getElementById('pdfInput');
    const uploadOverlay = document.getElementById('uploadOverlay');
    const dropZone = document.querySelector('.drop-zone');
    
    // State
    let pdfDoc = null;
    let pageNum = 1;
    let totalPages = 0;
    let pageStates = {}; // Stores drawings { 1: json, 2: json }
    let history = []; 
    let historyStep = -1;

    // --- 2. EVENT LISTENERS ---
    
    // Drag & Drop
    if (uploadOverlay) {
        uploadOverlay.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('drag-over'); });
        uploadOverlay.addEventListener('dragleave', (e) => { e.preventDefault(); dropZone.classList.remove('drag-over'); });
        uploadOverlay.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('drag-over');
            if (e.dataTransfer.files.length > 0 && e.dataTransfer.files[0].type === "application/pdf") {
                loadPDF(e.dataTransfer.files[0]);
            } else {
                alert("Please upload a PDF file.");
            }
        });
        
        // Click to Upload
        dropZone.addEventListener('click', () => pdfInput.click());
    }

    if (pdfInput) {
        pdfInput.addEventListener('change', (e) => { if(e.target.files[0]) loadPDF(e.target.files[0]); });
    }

    // Keyboard Shortcuts
    window.addEventListener('keydown', (e) => { if(e.key === 'Delete') deleteSelected(); });

    // History Tracking
    canvas.on('object:added', saveHistory);
    canvas.on('object:modified', saveHistory);


    // --- 3. CORE FUNCTIONS ---

    async function loadPDF(file) {
        try {
            const reader = new FileReader();
            reader.onload = async function() {
                const typedarray = new Uint8Array(this.result);
                // Ensure PDF.js worker is pointed correctly
                pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.worker.min.js';
                
                pdfDoc = await pdfjsLib.getDocument(typedarray).promise;
                totalPages = pdfDoc.numPages;
                pageNum = 1;
                pageStates = {}; 
                
                await renderPage(1);
                if(uploadOverlay) uploadOverlay.style.display = 'none';
            };
            reader.readAsArrayBuffer(file);
        } catch (err) {
            alert("Error loading PDF: " + err.message);
        }
    }

    async function renderPage(num) {
        console.log("Rendering Page: " + num);
        
        // Save current state before switching
        if (pdfDoc && pageNum !== num) {
            pageStates[pageNum] = JSON.stringify(canvas);
        }

        pageNum = num;
        const indicator = document.getElementById('page-indicator');
        if(indicator) indicator.innerText = `Page ${pageNum} of ${totalPages}`;

        try {
            const page = await pdfDoc.getPage(num);
            const viewport = page.getViewport({ scale: 1.5 });
            
            // Hidden Canvas for PDF Rendering
            const hiddenCanvas = document.createElement('canvas');
            hiddenCanvas.width = viewport.width;
            hiddenCanvas.height = viewport.height;
            const ctx = hiddenCanvas.getContext('2d');

            ctx.fillStyle = "#ffffff";
            ctx.fillRect(0, 0, hiddenCanvas.width, hiddenCanvas.height);

            await page.render({ canvasContext: ctx, viewport: viewport }).promise;

            // Fabric Image Background
            const bgImage = new fabric.Image(hiddenCanvas, {
                originX: 'left',
                originY: 'top',
                scaleX: 1,
                scaleY: 1
            });

            canvas.setWidth(viewport.width);
            canvas.setHeight(viewport.height);
            canvas.clear(); 
            canvas.setBackgroundImage(bgImage, canvas.renderAll.bind(canvas));

            // Restore Annotations
            if (pageStates[num]) {
                canvas.loadFromJSON(pageStates[num], function() {
                    canvas.setBackgroundImage(bgImage, canvas.renderAll.bind(canvas));
                });
            }
        } catch (err) {
            console.error("Render Error:", err);
        }
    }

    // --- 4. EXPORTED TOOLS (Attached to Window for HTML Buttons) ---
    
    window.changePage = function(offset) {
        const newPage = pageNum + offset;
        if (newPage >= 1 && newPage <= totalPages) {
            pageStates[pageNum] = JSON.stringify(canvas);
            renderPage(newPage);
        }
    };

    window.addText = function() {
        canvas.isDrawingMode = false;
        const text = new fabric.IText('Type here', { left: 100, top: 100, fill: document.getElementById('colorPicker').value, fontSize: 20 });
        canvas.add(text); canvas.setActiveObject(text);
    };

    window.toggleDraw = function() {
        canvas.isDrawingMode = !canvas.isDrawingMode;
        if(canvas.isDrawingMode) { 
            canvas.freeDrawingBrush.width = 5; 
            canvas.freeDrawingBrush.color = document.getElementById('colorPicker').value; 
        }
    };

    window.updateColor = function(val) {
        canvas.freeDrawingBrush.color = val;
        const obj = canvas.getActiveObject();
        if(obj) { obj.set({fill: val}); canvas.renderAll(); }
    };

    window.deleteSelected = function() { 
        const obj = canvas.getActiveObject(); 
        if(obj) canvas.remove(obj); 
    };
    
    window.undo = function() {
        canvas.isDrawingMode = false;
        if (historyStep > 0) {
            historyStep--;
            canvas.loadFromJSON(history[historyStep], canvas.renderAll.bind(canvas));
        }
    };

    function saveHistory() {
        if(historyStep < history.length - 1) history = history.slice(0, historyStep + 1);
        history.push(JSON.stringify(canvas));
        historyStep++;
    }

    // Save/Download Logic
    window.saveAllPages = async function() {
        const btn = document.querySelector('.save-btn');
        btn.innerText = "⏳ PROCESSING...";
        
        pageStates[pageNum] = JSON.stringify(canvas); // Save current page

        const { jsPDF } = window.jspdf;
        const pdf = new jsPDF({ orientation: 'p', unit: 'px', format: [canvas.width, canvas.height] });

        for (let i = 1; i <= totalPages; i++) {
            if (i > 1) pdf.addPage([canvas.width, canvas.height]);
            
            // Re-render page logic specifically for PDF generation...
            // (Uses the same logic as renderPageToPDF we wrote before)
            await renderPageToPDF(i, pdf); 
        }

        pdf.save('Zen_MultiPage_Edit.pdf');
        btn.innerText = "DOWNLOAD PDF";
        renderPage(pageNum);
    };

    async function renderPageToPDF(num, pdfObj) {
        const page = await pdfDoc.getPage(num);
        const viewport = page.getViewport({ scale: 1.5 });
        const tempCanvas = document.createElement('canvas');
        tempCanvas.width = viewport.width;
        tempCanvas.height = viewport.height;
        const ctx = tempCanvas.getContext('2d');
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);
        await page.render({ canvasContext: ctx, viewport: viewport }).promise;

        if (pageStates[num]) {
            const tempFabric = new fabric.StaticCanvas(null, { width: viewport.width, height: viewport.height });
            await new Promise(resolve => {
                tempFabric.loadFromJSON(pageStates[num], () => {
                    const bgImg = new fabric.Image(tempCanvas);
                    tempFabric.setBackgroundImage(bgImg, () => {
                        tempFabric.renderAll();
                        const imgData = tempFabric.toDataURL({ format: 'jpeg', quality: 0.8 });
                        pdfObj.addImage(imgData, 'JPEG', 0, 0, viewport.width, viewport.height);
                        resolve();
                    });
                });
            });
        } else {
            const imgData = tempCanvas.toDataURL('image/jpeg', 0.8);
            pdfObj.addImage(imgData, 'JPEG', 0, 0, viewport.width, viewport.height);
        }
    }
    
    // -- Shapes --
    window.addRect = function() { canvas.isDrawingMode = false; canvas.add(new fabric.Rect({ left: 100, top: 100, fill: 'transparent', stroke: 'red', strokeWidth: 2, width: 100, height: 100 })); };
    window.addCircle = function() { canvas.isDrawingMode = false; canvas.add(new fabric.Circle({ left: 100, top: 100, fill: 'transparent', stroke: 'red', strokeWidth: 2, radius: 50 })); };
    window.addArrow = function() { canvas.isDrawingMode = false; canvas.add(new fabric.Line([50, 50, 200, 50], { stroke: 'red', strokeWidth: 3 })); };
    window.addLine = function() { canvas.isDrawingMode = false; canvas.add(new fabric.Line([50, 50, 200, 50], { stroke: '#000', strokeWidth: 2 })); };
    window.activateWhiteout = function() { canvas.isDrawingMode = false; canvas.add(new fabric.Rect({ left: 100, top: 100, fill: 'white', width: 100, height: 30 })); };
    window.activateHighlight = function() { canvas.isDrawingMode = false; canvas.add(new fabric.Rect({ left: 100, top: 100, fill: 'yellow', width: 100, height: 30, opacity: 0.4 })); };

});