import os
import fitz  # PyMuPDF

class PDFCompressor:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder

    def process(self, input_path, output_filename, quality=None):
        """
        Compresses PDF using PyMuPDF (fitz).
        Uses garbage collection (level 4) to deduplicate streams and remove unused objects.
        """
        try:
            # Open the PDF
            doc = fitz.open(input_path)
            
            output_path = os.path.join(self.upload_folder, output_filename)
            
            # Save with maximum optimization
            # garbage=4: Aggressive deduplication and cleanup
            # deflate=True: Compress all streams
            doc.save(output_path, garbage=4, deflate=True)
            doc.close()
            
            return output_filename
            
        except Exception as e:
            print(f"Compression Error: {str(e)}")
            return None