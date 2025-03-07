import os
from fpdf import FPDF
from PIL import Image
import re

# ✅ Function to convert image to proper JPEG format
def convert_to_jpeg(image_path):
    try:
        with Image.open(image_path) as img:
            rgb_img = img.convert("RGB")  # Ensure RGB mode
            new_path = image_path.replace(".jpg", "_fixed.jpg")
            rgb_img.save(new_path, "JPEG")
            return new_path  # Return fixed image path
    except Exception as e:
        print(f"❌ Failed to convert {image_path}: {e}")
        return None


# ✅ Function to sort images numerically
def sort_numerically(file_list):
    def extract_number(filename):
        match = re.search(r'(\d+)', filename)  # Extracts first number found
        return int(match.group()) if match else float('inf')  # Convert to int for sorting

    return sorted(file_list, key=extract_number)


# ✅ Function to sanitize filenames (removes invalid characters for Windows)
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)


# ✅ Function to create PDF with properly ordered images
def create_pdf(image_folder, output_pdf):
    if not os.path.exists(image_folder):
        print("❌ Image folder does not exist. Cannot create PDF.")
        return

    pdf = FPDF()
    image_files = sort_numerically([f for f in os.listdir(image_folder) if f.endswith(".jpg")])

    temp_files = []  # Track temp fixed images for cleanup

    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        new_image_path = convert_to_jpeg(image_path) or image_path  # Convert if needed

        if new_image_path != image_path:
            temp_files.append(new_image_path)  # Store temp file

        with Image.open(new_image_path) as img:
            width, height = img.size

        pdf.add_page()
        pdf.image(new_image_path, x=0, y=0, w=210, h=height * (210 / width))  # Fit to A4 width

    if len(pdf.pages) > 0:
        safe_pdf_name = sanitize_filename(output_pdf)  # ✅ Sanitize output filename
        pdf.output(safe_pdf_name)
        print(f"✅ PDF created successfully: {safe_pdf_name}")
    else:
        print("❌ No valid images to create a PDF!")

    # ✅ Cleanup temp converted images
    for temp_file in temp_files:
        os.remove(temp_file)


# ✅ Main execution
if __name__ == "__main__":
    images_folder = "downloads"
    pdf_filename = "manga_chapter.pdf"
    create_pdf(images_folder, pdf_filename)
