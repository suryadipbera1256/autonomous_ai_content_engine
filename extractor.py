"""This is the first module of our LinkedIn Bot. We will use Selenium to log into LinkedIn,
navigate to the feed, and extract the text content of the top 5 posts."""
import os
import time
from dotenv import load_dotenv
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()
LINKEDIN_USER = os.getenv("LINKEDIN_USER")
LINKEDIN_PASS = os.getenv("LINKEDIN_PASS")

def scrape_linkedin_feed():
    print("Initializing stealth browser with Persistent Profile...")
    
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    
    # CRITICAL FIX: Create a persistent profile to save cookies. 
    # This makes the browser look 100% human and remembers your login!
    profile_path = os.path.join(os.getcwd(), "chrome_profile")
    options.add_argument(f"--user-data-dir={profile_path}")
    
    driver = uc.Chrome(options=options, version_main=145)

    try:
        print("Warming up browser network stack...")
        driver.get("https://www.google.com")
        time.sleep(3) 
        
        # Navigate to the main page first to accept initial tracking cookies
        print("Accessing LinkedIn homepage...")
        driver.get("https://www.linkedin.com/")
        time.sleep(4)
        
        # Check if we are already logged in from a previous session!
        if "feed" not in driver.current_url:
            print("Logging in...")
            driver.get("https://www.linkedin.com/login")
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            ).send_keys(LINKEDIN_USER)
            
            driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASS)
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
        else:
            print("Persistent profile detected: Already logged in!")

        print("Waiting for feed to populate...")
        print("(If LinkedIn asks for a verification code, solve it in the browser. The script will wait.)")
        
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.feed-shared-update-v2"))
        )
        time.sleep(3) 

        print("Extracting posts...")
        posts = driver.find_elements(By.CSS_SELECTOR, "div.feed-shared-update-v2")
        
        extracted_texts = []
        for post in posts[:5]: 
            try:
                text_element = post.find_element(By.CSS_SELECTOR, "div.update-components-text")
                if text_element.text.strip():
                    extracted_texts.append(text_element.text.strip())
            except Exception:
                continue
        
        return extracted_texts

    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    feed_data = scrape_linkedin_feed()
    if feed_data:
        print(f"\nSuccessfully extracted {len(feed_data)} posts:\n")