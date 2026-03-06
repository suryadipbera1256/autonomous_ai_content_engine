"""
Phase 2: The Brain.
Takes the extracted posts, analyzes the underlying themes, and writes a highly professional LinkedIn post.
Also generates an OVERLAY_TEXT hook and a HYPER-REALISTIC IMAGE_PROMPT.
"""
import os
from google import genai
from dotenv import load_dotenv

# Load credentials securely from the .env file
load_dotenv()

# Initialize the Google GenAI Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_and_generate(scraped_texts):
    print("Waking up the AI Brain...")
    
    # Combine the scraped texts into one readable block for the AI
    context = "\n\n".join(scraped_texts)
    
    # THE HYPER-REALISTIC "SECRET SAUCE" UPGRADE
    # This prompt provides a complete matrix for photorealistic image generation
    prompt = f"""
    You are an expert Data Scientist and AI/ML Engineer creating content for your professional LinkedIn profile. 
    Read the following recent posts from your feed:
    
    {context}
    
    Analyze the themes. Then, output YOUR response EXACTLY following this strict template format below. Do not add any extra text outside this template.

    [Write your engaging 150-word LinkedIn post here. NO MARKDOWN ASTERISKS. Use ALL CAPS for emphasis. Use Unicode emojis for bullets.]
    
    OVERLAY_TEXT: [Write exactly 5 to 7 words summarizing the core concept. NO MORE THAN 7 WORDS.]
    IMAGE_PROMPT: [Write your detailed, photorealistic prompt string using the complex structure below.]
    
    CRITICAL IMAGE PROMPT STRUCTURE FOR PHOTOREALISM:
    Construct the IMAGE_PROMPT string by combining components from this exact formula:
    [Subject Description] + [Environment/Background] + [Lighting Conditions] + [Camera Technicals] + [Texture/Detail Keywords]
    
    1. THE SUBJECT DESCRIPTION:
       A candid, full-shot of an AI professional, Data Scientist, or ML Engineer in action. Be specific (e.g., 'A professional man in his late 20s with glasses,' 'A woman with her hair pulled back focused on code,' 'A presenter on a minimalist corporate stage').
    
    2. ENVIRONMENT/BACKGROUND:
       Choose a realistic setting relevant to Data Science. Examples: modern data center in Bengaluru, India; minimalist startup office; upscale city cafe (like your example); or a corporate meeting room.
    
    3. LIGHTING CONDITIONS (The #1 giveaway):
       Specify ONE: natural golden hour sun, soft diffused window light, hard cinematic street lighting, or professional studio lighting.
    
    4. CAMERA TECHNICALS (Force optical physics):
       You MUST include ALL of these: 'Captured on a Sony A7R IV, 85mm lens, f/1.8 aperture.' (Use 35mm for wider office shots, 85mm for candid portraits). specify '8k resolution', 'no distortion', and 'cinematic color grading'.
    
    5. TEXTURE/DETAIL KEYWORDS (Eliminate the plastic look):
       You MUST include ALL of these: 'Features visible skin pores, fine fabric textures, realistic depth of field with soft bokeh background, micro-details like dust particles and moisture, shot on film grain.' (Optional: add 'Kodak Portra 400' or 'Leica M11' for specific profiles).
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error connecting to AI: {e}"

if __name__ == "__main__":
    # Test data
    test_data = ["AI is revolutionizing how we handle predictive analytics in data centers."]
    output = analyze_and_generate(test_data)
    print("\n--- AI Generated Content ---\n")
    print(output)