/* * FILE UPLOADER MODULE
 * Handles: Drag & Drop Visuals, File Input Changes
 */

document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.querySelector('.drop-zone');
    const fileInput = document.querySelector('input[type="file"]');

    if (dropZone && fileInput) {
        
        // --- 1. CLICK TO UPLOAD ---
        dropZone.addEventListener('click', () => fileInput.click());

        // --- 2. DRAG & DROP VISUALS ---
        
        // Drag Over (Show Glow)
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('drag-over');
        });

        // Drag Leave (Remove Glow)
        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('drag-over');
        });

        // Drop (Handle File)
        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('drag-over');

            if (e.dataTransfer.files.length > 0) {
                // Assign files to the hidden input
                fileInput.files = e.dataTransfer.files;
                
                // Trigger the change event manually to update UI
                const event = new Event('change');
                fileInput.dispatchEvent(event);
            }
        });

        // --- 3. SHOW SELECTED FILE NAME ---
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                // Create a list of file names
                let fileListHtml = '';
                Array.from(this.files).forEach(file => {
                    fileListHtml += `
                        <div class="file-item-bar">
                            <span>📄 ${file.name}</span>
                            <span style="font-size: 0.8em; opacity: 0.7;">(${(file.size / 1024 / 1024).toFixed(2)} MB)</span>
                        </div>
                    `;
                });

                // Update Dropzone Text
                const dropText = dropZone.querySelector('p');
                if(dropText) dropText.innerHTML = fileListHtml;
                
                // Change Title to "Ready"
                const dropTitle = dropZone.querySelector('h3');
                if(dropTitle) {
                    dropTitle.innerText = "FILES READY";
                    dropTitle.style.color = "#66FCF1";
                }
            }
        });
    }
});