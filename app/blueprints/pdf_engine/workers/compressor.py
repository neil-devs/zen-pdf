import os
import fitz  # PyMuPDF
import io
from PIL import Image

class PDFCompressor:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder

    def process(self, input_path, output_filename, quality=40):
        """
        Aggressive Compression:
        1. Extracts every image from the PDF.
        2. Compresses it to a low-quality JPEG using Pillow.
        3. Replaces the original image with the small one.
        4. Saves with garbage collection to remove unused data.
        """
        try:
            doc = fitz.open(input_path)
            
            # Iterate through every page
            for page in doc:
                image_list = page.get_images(full=True)
                
                # Check every image on the page
                for img_info in image_list:
                    xref = img_info[0] # The internal ID of the image
                    
                    try:
                        # Extract the raw image
                        base_image = doc.extract_image(xref)
                        image_bytes = base_image["image"]
                        
                        # Open with Pillow to compress it
                        img = Image.open(io.BytesIO(image_bytes))
                        
                        # Skip tiny icons to save time (keep them as is)
                        if img.width < 150 or img.height < 150:
                            continue
                            
                        # Prepare a buffer for the new compressed image
                        buffer = io.BytesIO()
                        
                        # Convert to RGB (JPEG doesn't support transparency)
                        if img.mode != "RGB":
                            img = img.convert("RGB")
                        
                        # COMPRESS: Save as JPEG with low quality (40%)
                        img.save(buffer, format="JPEG", quality=quality, optimize=True)
                        new_image_bytes = buffer.getvalue()
                        
                        # Replace the old heavy image stream with the new light one
                        doc.update_stream(xref, new_image_bytes)
                        
                    except Exception as img_err:
                        # If an image fails, just skip it and move to the next
                        print(f"Image Skip: {img_err}")
                        continue

            output_path = os.path.join(self.upload_folder, output_filename)
            
            # Final Save: 'garbage=4' removes the old deleted image data
            doc.save(output_path, garbage=4, deflate=True)
            doc.close()
            
            return output_filename
            
        except Exception as e:
            print(f"Compression Error: {str(e)}")
            return None