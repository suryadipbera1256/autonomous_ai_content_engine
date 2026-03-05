import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load credentials securely from the .env file
load_dotenv()
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

def generate_image(prompt):
    print(f"Waking up the Image Creator...\nPrompt: '{prompt}'")
    print("Please wait, the AI model might take 1-2 minutes to wake up if it's sleeping...")
    
    try:
        # Initialize the official Hugging Face client
        client = InferenceClient(token=HF_API_KEY)
        
        # We use the text_to_image function directly
        image = client.text_to_image(
            prompt,
            model="stabilityai/stable-diffusion-xl-base-1.0"
        )
        
        # Save the image locally
        filename = "generated_post_image.png"
        image.save(filename)
        
        print(f"Success! Image securely saved as '{filename}'.")
        return filename
            
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

if __name__ == "__main__":
    # Our predictive maintenance test prompt
    test_prompt = "A high-quality 3D render of a futuristic predictive maintenance dashboard for a factory, glowing data visualizations, machine learning concept art, photorealistic, 8k resolution"
    
    generate_image(test_prompt)