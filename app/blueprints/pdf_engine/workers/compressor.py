import os
import pikepdf
import io
from PIL import Image

class PDFCompressor:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder

    def process(self, input_path, output_filename, quality=50):
        """
        Compresses PDF by:
        1. Linearizing (Fast Web View)
        2. Discarding unused resources
        3. Re-encoding images to JPEG with lower quality (Aggressive)
        """
        try:
            # Open PDF
            pdf = pikepdf.open(input_path)
            
            # --- 1. Aggressive Image Compression ---
            # We iterate over all pages and find images to squash
            for page in pdf.pages:
                for name, image in page.images.items():
                    # We only compress large images to save time/risk
                    # Filter: Must be an image and not a tiny icon
                    if image.Filter != '/DCTDecode' and image.Width > 100 and image.Height > 100:
                        continue 

                    try:
                        # Extract image using Pillow
                        raw_image = pikepdf.PdfImage(image)
                        pil_image = raw_image.as_pil_image()

                        # Create a buffer to save the compressed version
                        buffer = io.BytesIO()
                        
                        # Convert to RGB (PDFs handle RGB JPEGs best)
                        if pil_image.mode != 'RGB':
                            pil_image = pil_image.convert('RGB')

                        # Save as JPEG with lower quality (50 is standard for "Strong" compression)
                        pil_image.save(buffer, format="JPEG", quality=quality, optimize=True)
                        
                        # Replace the old image in the PDF with the new lightweight one
                        new_image = pikepdf.PdfImage(
                            io.BytesIO(buffer.getvalue())
                        )
                        # We replace the internal object directly
                        image.write(new_image.obj, pdf)
                        
                    except Exception as img_err:
                        # If an image fails, skip it and continue to the next
                        # print(f"Skipped an image due to: {img_err}")
                        continue

            # --- 2. Structural Cleanup ---
            pdf.remove_unreferenced_resources()
            
            output_path = os.path.join(self.upload_folder, output_filename)
            
            # --- 3. Save with efficient stream packing ---
            pdf.save(
                output_path, 
                compress_streams=True, 
                object_stream_mode=pikepdf.ObjectStreamMode.generate
            )
            
            return output_filename
            
        except Exception as e:
            print(f"Compression Error: {str(e)}")
            return None