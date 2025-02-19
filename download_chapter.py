import os
import requests
from PIL import Image

BASE_URL = "https://api.mangadex.org"

# ✅ Function to download images with progress tracking
def download_chapter_images(chapter_id, save_folder="downloads", progress_callback=None):
    os.makedirs(save_folder, exist_ok=True)

    at_home_url = f"{BASE_URL}/at-home/server/{chapter_id}"
    response = requests.get(at_home_url)
    if response.status_code != 200:
        print(f"❌ Failed to fetch chapter data: {response.status_code}")
        return []

    chapter_data = response.json()
    image_urls = chapter_data.get("chapter", {}).get("data", [])

    valid_images = []  # Store valid image paths
    temp_images = []  # Temporary list for merging

    total_images = len(image_urls)  # Total images for progress tracking

    for index, image_name in enumerate(image_urls):
        image_url = f"{chapter_data['baseUrl']}/data/{chapter_data['chapter']['hash']}/{image_name}"
        image_path = os.path.join(save_folder, f"{index+1}.jpg")

        # ✅ Download the image
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(image_path, "wb") as img_file:
                img_file.write(response.content)

            # ✅ Verify image integrity
            if is_valid_image(image_path):
                print(f"✅ Downloaded: {image_path}")
                temp_images.append(image_path)  # Add to temp list

                # Check and merge dual images if needed
                if len(temp_images) == 2:
                    merged_image = merge_dual_images(temp_images[0], temp_images[1])
                    if merged_image:
                        valid_images.append(merged_image)
                        temp_images.clear()
                    else:
                        valid_images.extend(temp_images)
                        temp_images.clear()

            else:
                print(f"❌ Corrupt image detected: {image_path}. Deleting...")
                os.remove(image_path)

        else:
            print(f"❌ Failed to download: {image_url}")

        # ✅ Update progress
        if progress_callback:
            progress_percentage = int(((index + 1) / total_images) * 100)
            progress_callback(progress_percentage)

    # If an unpaired image remains, add it normally
    valid_images.extend(temp_images)

    # ✅ Ensure progress bar reaches 100% at the end
    if progress_callback:
        progress_callback(100)

    return valid_images


# ✅ Function to check if an image is valid
def is_valid_image(image_path):
    try:
        with Image.open(image_path) as img:
            img.verify()
        return True
    except Exception as e:
        print(f"❌ Invalid image: {image_path} - Error: {e}")
        return False


# ✅ Function to merge two images if they are dual pages
def merge_dual_images(img1_path, img2_path):
    try:
        img1 = Image.open(img1_path)
        img2 = Image.open(img2_path)

        if img1.width >= img1.height * 1.9 and img2.width >= img2.height * 1.9:
            print(f"🔄 Merging dual pages: {img1_path} + {img2_path}")

            merged_width = img1.width + img2.width
            merged_height = max(img1.height, img2.height)
            merged_image = Image.new("RGB", (merged_width, merged_height))

            merged_image.paste(img1, (0, 0))
            merged_image.paste(img2, (img1.width, 0))

            merged_path = img1_path.replace(".jpg", "_merged.jpg")
            merged_image.save(merged_path, "JPEG")

            os.remove(img1_path)
            os.remove(img2_path)

            return merged_path
    except Exception as e:
        print(f"❌ Error merging images: {e}")

    return None


# ✅ Main execution for testing
if __name__ == "__main__":
    chapter_id = "e7c4d0c9-cec9-4116-aba1-178b2a5d4cc3"  # Example chapter
    download_chapter_images(chapter_id, progress_callback=lambda x: print(f"Progress: {x}%"))
