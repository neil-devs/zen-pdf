import os
import fitz  # PyMuPDF
import io
from PIL import Image

class PDFCompressor:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder

    def process(self, input_path, output_filename, quality=40):
        """
        Ultimate Local Compression:
        1. Opens PDF with PyMuPDF.
        2. Extracts every image.
        3. Crushes images using Pillow (JPEG 40% Quality).
        4. Rebuilds the PDF with high-level garbage collection.
        """
        try:
            doc = fitz.open(input_path)
            
            for page in doc:
                image_list = page.get_images(full=True)
                
                for img_info in image_list:
                    xref = img_info[0]
                    try:
                        base_image = doc.extract_image(xref)
                        image_bytes = base_image["image"]
                        
                        img = Image.open(io.BytesIO(image_bytes))
                        
                        # Skip small icons
                        if img.width < 150 or img.height < 150:
                            continue
                            
                        buffer = io.BytesIO()
                        if img.mode != "RGB":
                            img = img.convert("RGB")
                        
                        # Aggressive Compression
                        img.save(buffer, format="JPEG", quality=quality, optimize=True)
                        new_image_bytes = buffer.getvalue()
                        
                        doc.update_stream(xref, new_image_bytes)
                        
                    except Exception as e:
                        continue

            output_path = os.path.join(self.upload_folder, output_filename)
            # Maximum optimization
            doc.save(output_path, garbage=4, deflate=True)
            doc.close()
            
            return output_filename
            
        except Exception as e:
            print(f"Local Compression Error: {str(e)}")
            return None