import os
from PIL import Image

class ImageToPDF:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder

    def process(self, image_paths, output_filename):
        """
        Converts a list of images into a single PDF.
        """
        try:
            if not image_paths:
                return None

            # Open all images and convert to RGB (PDF requirement)
            images = []
            for path in image_paths:
                img = Image.open(path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                images.append(img)

            output_path = os.path.join(self.upload_folder, output_filename)

            # Save first image and append the rest
            images[0].save(
                output_path, 
                "PDF", 
                resolution=100.0, 
                save_all=True, 
                append_images=images[1:]
            )
            
            return output_filename
            
        except Exception as e:
            print(f"Convert Error: {str(e)}")
            return None