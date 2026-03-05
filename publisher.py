import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")

# 🕵️ STEALTH HEADERS: Hide the "python-requests" default User-Agent
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "X-Restli-Protocol-Version": "2.0.0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def publish_to_linkedin(text_content, image_path):
    print("Initiating LinkedIn Publishing Sequence...")

    # 1. Get User URN
    print("Authenticating...")
    user_resp = requests.get("https://api.linkedin.com/v2/userinfo", headers=HEADERS)
    if user_resp.status_code != 200:
        return print(f"Auth failed: {user_resp.json()}")
    author_urn = f"urn:li:person:{user_resp.json()['sub']}"

    # 2. Register Image Upload
    print("Registering image with LinkedIn servers...")
    register_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
    register_payload = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "owner": author_urn,
            "serviceRelationships": [{"relationshipType": "OWNER", "identifier": "urn:li:userGeneratedContent"}]
        }
    }
    reg_resp = requests.post(register_url, headers=HEADERS, json=register_payload).json()
    upload_url = reg_resp['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
    asset_urn = reg_resp['value']['asset']

    # 3. Upload the actual image file
    print("Waiting 3 seconds for LinkedIn CDN to provision the URL...")
    import time
    time.sleep(3) # CRITICAL: Gives the server time to prepare for the binary
    
    print("Uploading image binary...")
    with open(image_path, 'rb') as file:
        image_data = file.read() 
        
    upload_headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/octet-stream",
        "Connection": "close" # Prevents stale socket resets
    }
    
    upload_resp = requests.put(upload_url, headers=upload_headers, data=image_data)
    
    if upload_resp.status_code != 201:
        print(f"❌ Image upload failed: {upload_resp.status_code} - {upload_resp.text}")
        return

if __name__ == "__main__":
    # Test Data: We will use a dummy text and the image you just generated
    test_text = "Testing my custom end-to-end AI content automation pipeline! Built with Python, Selenium, Gemini 2.5, and Stable Diffusion."
    test_image = "generated_post_image.png"
    
    # IMPORTANT: Running this will actually post to your real LinkedIn profile!
    publish_to_linkedin(test_text, test_image)