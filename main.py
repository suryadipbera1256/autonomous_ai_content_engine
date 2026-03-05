from extractor import scrape_linkedin_feed
from brain import analyze_and_generate
from creator import generate_image
from publisher import publish_to_linkedin

def run_automation_pipeline():
    print("\n==================================================")
    print("🚀 STARTING AI CONTENT AUTOMATION PIPELINE")
    print("==================================================\n")
    
    # 1. Extract fresh data
    print("Step 1: Extracting trending data from feed...")
    feed_data = scrape_linkedin_feed()
    if not feed_data:
        print("❌ No data extracted. Aborting this run.")
        return

    # 2. Brain (Analyze and write)
    print("\nStep 2: AI is analyzing data and writing content...")
    ai_output = analyze_and_generate(feed_data)
    
    if "IMAGE_PROMPT:" not in ai_output:
        print("❌ Error: AI did not format the output correctly. Aborting.")
        return
        
    parts = ai_output.split("IMAGE_PROMPT:")
    post_text = parts[0].strip()
    image_prompt = parts[1].strip()
    
    print(f"✅ Content generated. Image prompt extracted:\n'{image_prompt}'")

    # 3. Creator (Generate unique image)
    print("\nStep 3: Generating new image from prompt...")
    image_path = generate_image(image_prompt)
    if not image_path:
        print("❌ Image generation failed. Aborting.")
        return

    # 4. Publisher (Post to LinkedIn)
    print("\nStep 4: Publishing to LinkedIn...")
    publish_to_linkedin(post_text, image_path)
    
    print("\n==================================================")
    print("✨ PIPELINE RUN COMPLETE")
    print("==================================================\n")

if __name__ == "__main__":
    run_automation_pipeline()