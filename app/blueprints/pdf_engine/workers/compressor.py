import os
from pypdf import PdfReader, PdfWriter

class PDFCompressor:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder

    def process(self, input_path, output_filename, quality=None):
        """
        Compresses PDF using pypdf.
        This function signature matches your project structure perfectly.
        Other files (like routes.py) will call this 'process' function 
        and it will work without changes.
        """
        try:
            reader = PdfReader(input_path)
            writer = PdfWriter()

            # Cycle through every page and apply compression
            for page in reader.pages:
                # This compresses text and vector commands inside the PDF
                page.compress_content_streams()
                writer.add_page(page)

            # Define output path
            output_path = os.path.join(self.upload_folder, output_filename)
            
            # Write the file with compression enabled
            with open(output_path, "wb") as f:
                writer.write(f)
            
            writer.close()
            return output_filename
            
        except Exception as e:
            print(f"Compression Error: {str(e)}")
            return None