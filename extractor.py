"""This is the first module of our LinkedIn Bot. We will use Selenium to log into LinkedIn,
navigate to a global keyword search, and extract the text content using injected JavaScript."""
import os
import time
import random # <-- NEW: Added to enable dynamic topic selection
from dotenv import load_dotenv
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

load_dotenv()
LINKEDIN_USER = os.getenv("LINKEDIN_USER")
LINKEDIN_PASS = os.getenv("LINKEDIN_PASS")

# 🎯 THE EXPERT TOPIC MATRIX
# A comprehensive list of advanced Data Science, AI, and MLOps keywords
AI_TOPICS = [
    # Core Data Science & ML
    "Data Science", "Machine Learning", "Deep Learning", "Predictive Modeling",
    "Artificial Neural Networks", "Convolutional Neural Networks", "Recurrent Neural Networks", 
    "Transformers", "Attention Mechanisms", 

    # Advanced Deep Learning & Architectures
    "Deep Learning Architectures", "Convolutional Neural Networks", "Artificial Neural Networks",
    "Transfer Learning", "Neural Network Optimization", "Transformer Models",
    
    # Practical MLOps & Engineering (Showing you can build real things)
    "AI Microservices", "Dockerizing ML Models", "Flask API for AI", "Edge AI",
    "ML System Design", "Continuous Model Training", "AI Backend Architecture",
    
    # Predictive Modeling & Real-World Application
    "Predictive Maintenance AI", "IoT Machine Learning", "XGBoost", "Tree-Based Models",
    "Time Series Forecasting", "Anomaly Detection", "Sensor Data Analytics",
    
    # Trust, Interpretation, & Fundamentals
    "Explainable AI", "SHAP Values", "Algorithmic Efficiency", "AI Governance",
    "Responsible AI", "Model Interpretability", "Data Structures in ML",
    # Generative AI & LLMs
    "Generative AI", "Large Language Models", "Prompt Engineering", 
    "Generative Adversarial Networks", "NLP", "AI Agents", "Retrieval-Augmented Generation", 
    
    # Engineering, MLOps & Tools
    "MLOps", "AI Infrastructure", "Data Engineering", "Model Deployment",
    "Hugging Face", "PyTorch", "TensorFlow", "LangChain", "Agentic AI", "Multi-Agent Systems", 
    "Retrieval-Augmented Generation", "RAG Pipelines", "Small Language Models", "Multimodal AI", 
    "Fine-Tuning LLMs", "Vector Databases","Autonomous AI Agents", "Local LLMs", "AI Orchestration",
    "AI Workflow Automation", "AI-Driven Data Pipelines",
    
    # Applied AI & Industry
    "AI Automation", "IoT Predictive Maintenance", "Data Analytics", 
    "Computer Vision", "AI Ethics"
]

# Dynamically select ONE random topic for this specific execution cycle
TARGET_KEYWORD = random.choice(AI_TOPICS)

def scrape_linkedin_feed():
    print("Initializing stealth browser with Persistent Profile...")    
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    
    profile_path = os.path.join(os.getcwd(), "chrome_profile")
    options.add_argument(f"--user-data-dir={profile_path}")
    
    driver = uc.Chrome(options=options, version_main=145)

    try:
        print("Warming up browser network stack...")
        driver.get("https://www.google.com")
        time.sleep(3) 
        
        print("Accessing LinkedIn homepage...")
        driver.get("https://www.linkedin.com/")
        time.sleep(5) 
        
        # Check if we are already logged in
        if "feed" not in driver.current_url:
            print("Logging in...")
            driver.get("https://www.linkedin.com/login")
            
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "username"))
                ).send_keys(LINKEDIN_USER)
                
                driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASS)
                driver.find_element(By.XPATH, "//button[@type='submit']").click()
                print("Credentials submitted.")
            except TimeoutException:
                print("\n⚠️ [SECURITY INTERCEPTION DETECTED]")
                print("LinkedIn is showing a CAPTCHA or a 'Welcome Back' screen.")
                print("⏸️ ACTION REQUIRED: Please look at the Chrome window and manually log in or solve the puzzle.")
                print("⏳ The script will wait patiently...\n")
        else:
            print("Persistent profile detected: Already logged in!")

        # --- CRITICAL UPGRADE: KEYWORD SEARCH URL ---
        print(f"Navigating to global network feed for '{TARGET_KEYWORD}'...")
        # A keyword search provides a much more stable DOM than a hashtag search
        driver.get(f"https://www.linkedin.com/search/results/content/?keywords={TARGET_KEYWORD}")
        time.sleep(8) # Wait for initial heavy page load
        
        print("Scrolling aggressively to trigger lazy-loaded posts...")
        # Scroll up and down to trick the page into rendering the content
        for i in range(4):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 600);")
            time.sleep(2)

        print("Executing JavaScript Bulldozer to extract text...")
        
        # --- THE FIX: JAVASCRIPT INJECTION ---
        # Instead of waiting for a specific brittle class, we inject JS to read the whole page.
        # This completely eliminates the TimeoutException!
        js_script = """
            let results = [];
            // Target ANY element that commonly holds text
            let nodes = document.querySelectorAll('span[dir="ltr"], div.update-components-text, span.break-words');
            
            nodes.forEach(node => {
                let text = node.innerText.trim();
                // If it's a long paragraph (a real post) and we haven't saved it yet
                if (text.length > 100 && !results.includes(text)) {
                    results.push(text);
                }
            });
            return results;
        """
        
        extracted_texts = driver.execute_script(js_script)
        
        # If the specific classes failed, fallback to ripping ALL large paragraphs on the page
        if not extracted_texts:
            print("Standard classes hidden. Falling back to Deep DOM extraction...")
            fallback_script = """
                let results = [];
                let allDivs = document.querySelectorAll('div, span');
                allDivs.forEach(node => {
                    let text = node.innerText.trim();
                    if (text.length > 150 && !results.includes(text) && text.split(' ').length > 20) {
                        results.push(text);
                    }
                });
                return results;
            """
            extracted_texts = driver.execute_script(fallback_script)

        return extracted_texts[:5]

    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    feed_data = scrape_linkedin_feed()
    if feed_data:
        print(f"\n✅ Successfully extracted {len(feed_data)} posts:\n")
        for i, text in enumerate(feed_data):
            print(f"--- Post {i+1} ---")
            print(f"{text[:100]}...\n")
    else:
        print("❌ No posts found. The feed might be empty or blocked.")