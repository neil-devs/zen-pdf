import os
from pypdf import PdfReader, PdfWriter

class PDFSplitter:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder

    def process(self, input_path, start_page, end_page, output_filename):
        """
        Extracts pages from start_page to end_page (1-based index).
        """
        try:
            reader = PdfReader(input_path)
            writer = PdfWriter()
            
            # Validation: Ensure pages exist
            total_pages = len(reader.pages)
            if start_page < 1 or end_page > total_pages:
                raise ValueError("Page range out of bounds")

            # Extract pages (adjust for 0-based index)
            for i in range(start_page - 1, end_page):
                writer.add_page(reader.pages[i])

            output_path = os.path.join(self.upload_folder, output_filename)
            
            with open(output_path, "wb") as f_out:
                writer.write(f_out)
                
            return output_filename
            
        except Exception as e:
            print(f"Split Error: {str(e)}")
            return None