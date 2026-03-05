"""
Now that we have the raw data, it is time to build Phase 2: The Brain.
 We are going to write a script that takes those two posts, analyzes the underlying themes (like career milestones or strategic thinking),
 and writes a highly professional LinkedIn post from the perspective of a Data Scientist and AI/ML Engineer.
"""
import os
from google import genai
from dotenv import load_dotenv

# Load credentials securely from the .env file
load_dotenv()

# Initialize the new Google GenAI Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_and_generate(scraped_texts):
    print("Waking up the AI Brain...")
    
    # Combine the scraped texts into one readable block for the AI
    context = "\n\n".join(scraped_texts)
    
    # The system prompt that acts as your ghostwriter
    prompt = f"""
    You are an expert Data Scientist and AI/ML Engineer creating content for your professional LinkedIn profile. 
    Read the following recent posts from your feed:
    
    {context}
    
    Step 1: Identify an underlying theme from these posts (e.g., career milestones, strategic thinking, data-driven architecture, or predictive modeling).
    Step 2: Write a single, engaging LinkedIn post (about 150 words) that connects this theme to Data Science or Artificial Intelligence. Make it insightful and professional. Do not use hashtags.
    Step 3: At the very bottom, write a highly detailed 1-2 sentence image generation prompt that visually represents this post. Label it exactly as "IMAGE_PROMPT:".
    """
    
    try:
        # Using the new SDK syntax and the current Gemini 2.5 Flash model
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error connecting to AI: {e}"

if __name__ == "__main__":
    # We are passing in the exact data you just scraped to test it
    test_data = [
        "𝑩𝒆𝒊𝒏𝒈 𝑰𝒏𝒇𝒊𝒏𝒊𝒕𝒚 𝑺𝑫𝑬 𝑰𝒏𝒕𝒆𝒓𝒏𝒔𝒉𝒊𝒑 – 𝑶𝒏𝒍𝒊𝒏𝒆 𝑨𝒔𝒔𝒆𝒔𝒔𝒎𝒆𝒏𝒕 #1\nThe first milestone in your Being Infinity – SDE Internship (2028 Graduating Batch) journey is h...",
        "𝐌𝐜𝐃𝐨𝐧𝐚𝐥𝐝'𝐬 removed 𝐚𝐥𝐥 𝐟𝐨𝐨𝐝 𝐢𝐦𝐚𝐠𝐞𝐬 during 𝐑𝐚𝐦𝐚𝐝𝐚𝐧.\nAnd won multiple marketing awards for it.\nThe Campaign:\n-McDonald's Germany cleared all billboards..."
    ]
    
    output = analyze_and_generate(test_data)
    print("\n--- AI Generated Content ---\n")
    print(output)