import os
import json
import hashlib
import time
import logging
from extractor import scrape_linkedin_feed
from brain import analyze_and_generate
from creator import generate_image
from publisher import publish_to_linkedin

# --- ENTERPRISE LOGGING SETUP ---
# This creates a 'bot_activity.log' file on your computer. 
# You can open it anytime to see exactly what the bot did in the background!
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("bot_activity.log", encoding='utf-8'),
        logging.StreamHandler() # Also print to terminal
    ]
)
logger = logging.getLogger(__name__)

MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_memory(memory_list):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory_list, f)

def get_text_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def run_automation_pipeline():
    logger.info("==================================================")
    logger.info("🚀 STARTING AI CONTENT AUTOMATION PIPELINE (V3.0)")
    logger.info("==================================================")
    
    logger.info("Step 1: Extracting trending data from feed...")
    feed_data = scrape_linkedin_feed()
    if not feed_data:
        logger.warning("❌ No data extracted. Network might be down.")
        return False # Return False triggers a retry

    logger.info("🧠 Checking Memory for duplicate posts...")
    memory = load_memory()
    new_posts = []
    
    for post in feed_data:
        post_hash = get_text_hash(post)
        if post_hash not in memory:
            new_posts.append(post)
            memory.append(post_hash)
            
    if not new_posts:
        logger.info("💤 No new posts found in feed. Bot is going back to sleep to prevent spam.")
        return True # Return True because the bot worked perfectly (just no new work to do)
        
    logger.info(f"✅ Found {len(new_posts)} brand new posts to analyze!")
    
    if len(memory) > 100:
        memory = memory[-100:]
    save_memory(memory)

    logger.info("Step 2: AI is analyzing data and writing content...")
    ai_output = analyze_and_generate(new_posts)
    
    if "IMAGE_PROMPT:" not in ai_output or "OVERLAY_TEXT:" not in ai_output:
        logger.error("❌ Error: AI did not format the output correctly.")
        return False
        
    try:
        post_parts = ai_output.split("OVERLAY_TEXT:")
        post_text = post_parts[0].strip()
        
        meta_parts = post_parts[1].split("IMAGE_PROMPT:")
        overlay_text = meta_parts[0].replace('"', '').replace('*', '').strip()
        image_prompt = meta_parts[1].strip()
        
        if len(overlay_text) > 65:
            overlay_text = overlay_text[:62] + "..."

    except Exception as e:
        logger.error(f"❌ Error parsing AI output: {e}")
        return False
    
    logger.info(f"✅ Content generated! Hook: '{overlay_text}'")

    logger.info("Step 3: Generating new image from prompt...")
    image_path = generate_image(image_prompt, overlay_text)
    if not image_path:
        logger.error("❌ Image generation failed. API might be asleep.")
        return False

    logger.info("Step 4: Publishing to LinkedIn...")
    try:
        success = publish_to_linkedin(post_text, image_path)
        if not success:
            logger.error("❌ Publishing API rejected the payload.")
            return False
            
        logger.info("✅ Successfully published to LinkedIn!")
    except Exception as e:
        logger.error(f"❌ Critical publishing failure: {e}")
        return False
    
    logger.info("✨ PIPELINE RUN COMPLETE")
    logger.info("==================================================\n")
    return True

if __name__ == "__main__":
    MAX_RETRIES = 3
    RETRY_DELAY = 60 # Wait 60 seconds before trying again
    
    # --- THE UNBREAKABLE RETRY LOOP ---
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"--- Execution Attempt {attempt}/{MAX_RETRIES} ---")
            
            # Run the pipeline
            pipeline_success = run_automation_pipeline()
            
            if pipeline_success:
                break # Everything worked perfectly! Exit the retry loop.
            else:
                logger.warning(f"⚠️ Pipeline aborted due to an internal error or network failure.")
                
        except Exception as e:
            # This catches massive crashes (like Selenium failing to open Chrome)
            logger.error(f"💥 CRITICAL PIPELINE CRASH: {e}")
            
        # If it failed and we still have retries left...
        if attempt < MAX_RETRIES:
            logger.info(f"⏳ Waiting {RETRY_DELAY} seconds before retrying...\n")
            time.sleep(RETRY_DELAY)
        else:
            logger.critical("🚨 Maximum retries reached. Shutting down bot until next scheduled run.")