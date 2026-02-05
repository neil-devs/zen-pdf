import os
from PyPDF2 import PdfWriter, PdfReader

class PDFMerger:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder

    def process(self, file_paths, output_filename):
        """
        Merges a list of PDF file paths into a single PDF.
        Returns the path to the result.
        """
        merger = PdfWriter()
        
        try:
            for path in file_paths:
                # Security Check: Ensure file exists
                if os.path.exists(path):
                    merger.append(path)
                else:
                    raise FileNotFoundError(f"File not found: {path}")

            # Define output path
            output_path = os.path.join(self.upload_folder, output_filename)
            
            # Write the result
            with open(output_path, "wb") as f_out:
                merger.write(f_out)
            
            merger.close()
            return output_filename
            
        except Exception as e:
            # In enterprise apps, we log this error properly
            print(f"Merge Error: {str(e)}")
            return None