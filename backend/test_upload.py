# test_upload.py
import requests

# Create a simple test image (or use any image file you have)
url = "http://localhost:8000/upload-image"

# Option 1: Upload from file
with open("test_image.png", "rb") as f:
    files = {"file": ("test.png", f, "image/png")}
    response = requests.post(url, files=files)
    print(response.json())

# Expected output:
# {
#   "success": true,
#   "url": "https://i.ibb.co/XXXXXXX/xxxxx.png",  # <-- This is what Replicate needs!
#   "filename": "uuid-here.png",
#   "message": "Image uploaded successfully"
# }