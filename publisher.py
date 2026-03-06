import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "X-Restli-Protocol-Version": "2.0.0"
}

def publish_to_linkedin(text_content, image_path):
    print("Initiating LinkedIn Publishing Sequence...")

    # 1. Get User URN
    print("Authenticating...")
    user_resp = requests.get("https://api.linkedin.com/v2/userinfo", headers=HEADERS)
    if user_resp.status_code != 200:
        print(f"Auth failed: {user_resp.json()}")
        return False # <-- Tell main.py it failed!

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
    print("Uploading image binary...")
    with open(image_path, 'rb') as file:
        image_data = file.read() 
        
    upload_headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "image/png" 
    }
    
    upload_resp = requests.put(upload_url, headers=upload_headers, data=image_data)
    
    if upload_resp.status_code != 201:
        print(f"❌ Image upload failed: {upload_resp.status_code} - {upload_resp.text}")
        return False # <-- Tell main.py it failed!

    # 4. Create the Post
    print("Publishing final post...")
    post_url = "https://api.linkedin.com/v2/ugcPosts"
    post_payload = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text_content},
                "shareMediaCategory": "IMAGE",
                "media": [{"status": "READY", "description": {"text": "AI Generated Image"}, "media": asset_urn}]
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }
    
    post_resp = requests.post(post_url, headers=HEADERS, json=post_payload)
    if post_resp.status_code == 201:
        print("Success! Your AI post is now live on LinkedIn.")
        return True # <-- Tell main.py it was a complete success!
    else:
        print(f"Failed to post: {post_resp.text}")
        return False