import os
import fitz  # PyMuPDF

class PDFCompressor:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder

    def process(self, input_path, output_filename, quality=None):
        """
        Safe Mode Compression (Render Free Tier Compatible).
        Uses PyMuPDF's internal optimization to reduce file size 
        without exploding memory usage.
        """
        try:
            doc = fitz.open(input_path)
            output_path = os.path.join(self.upload_folder, output_filename)
            
            # 'garbage=4' removes unused objects (very effective)
            # 'deflate=True' compresses the data streams
            # This runs entirely in C++ (low memory), not Python
            doc.save(output_path, garbage=4, deflate=True)
            doc.close()
            
            return output_filename
            
        except Exception as e:
            print(f"Compression Error: {str(e)}")
            return None