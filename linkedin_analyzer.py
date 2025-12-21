import pandas as pd
import time
import nltk
import sys
import getpass
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

# --- CONFIGURATION ---
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    print("Downloading VADER lexicon...")
    nltk.download('vader_lexicon')

def categorize_sentiment(sia, text):
    """
    Analyzes text and returns: 'Very Good', 'Good', 'Neutral', 'Bad', or 'Worst'
    """
    if not text:
        return "Neutral"
        
    scores = sia.polarity_scores(text)
    compound = scores['compound']
    
    if compound >= 0.5:
        return "Very Good"
    elif 0.05 <= compound < 0.5:
        return "Good"
    elif -0.05 < compound < 0.05:
        return "Neutral"
    elif -0.5 < compound <= -0.05:
        return "Bad"
    else:
        return "Worst"

def main():
    print("========================================")
    print("   LINKEDIN COMMENT SENTIMENT CLI")
    print("========================================")

    # 1. Setup Driver
    print("\n[1/4] Launching Browser...")
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3") 
    
    # --- FIX FOR GOOGLE AUTH BLOCKS ---
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # ----------------------------------

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception as e:
        print(f"Error launching Chrome: {e}")
        return

    # 2. Login Phase (Manual Only)
    driver.get("https://www.linkedin.com/login")
    print("\n[2/4] Login Required:")
    print("  -> A Chrome window has opened.")
    print("  -> ACTION REQUIRED: Please Log in to LinkedIn manually in that window.")
    print("  -> (You can safely use 'Sign in with Google' or email/password)")
    
    # Wait for user confirmation
    input("\n  -> Once you are successfully logged in and can see your feed, PRESS ENTER here to continue...")

    # 3. User Inputs (Multiple Selection)
    print("\n[3/4] Configuration:")
    post_url = input("  -> Paste the LinkedIn Post URL here: ").strip()
    
    print("\n  -> Which comments do you want to keep? (Enter multiple separated by commas)")
    print("     [1] Very Good  (High Praise)")
    print("     [2] Good       (Positive)")
    print("     [3] Bad        (Negative)")
    print("     [4] Worst      (Highly Critical)")
    print("     [5] ALL        (Keep Everything)")
    print("     Example: Enter '1,4' to get only Very Good and Worst comments.")
    
    user_choices = input("  -> Enter choices (e.g. 1,2): ").strip().split(',')
    
    # Map inputs to categories
    target_categories = []
    category_map = {
        '1': "Very Good",
        '2': "Good",
        '3': "Bad",
        '4': "Worst",
        '5': "ALL"
    }

    for choice in user_choices:
        c = choice.strip()
        if c in category_map:
            target_categories.append(category_map[c])
    
    if not target_categories or "ALL" in target_categories:
        target_categories = ["ALL"]

    print(f"\n[4/4] Starting scraper for categories: {target_categories}...")
    print("---------------------------------------------------------------")
    print("  !!! PRESS CTRL+C AT ANY TIME TO STOP AND SAVE TO EXCEL !!!")
    print("---------------------------------------------------------------")
    
    try:
        driver.get(post_url)
    except Exception as e:
        print(f"Invalid URL: {e}")
        try:
            driver.quit()
        except: pass
        return

    sia = SentimentIntensityAnalyzer()
    scraped_data = []
    seen_comments = set()
    
    # 5. Scraping Loop
    try:
        while True:
            # Click 'Load more'
            try:
                load_btns = driver.find_elements(By.XPATH, "//button[contains(@class, 'comments-comments-list__load-more-comments-button')]")
                for btn in load_btns:
                    if btn.is_displayed():
                        driver.execute_script("arguments[0].click();", btn)
                        time.sleep(1)
            except: pass

            # Find Comments
            # UPDATED: We now look specifically for 'comments-comment-item' class
            # This prevents scraping other posts/articles if you scroll down too far.
            try:
                comments = driver.find_elements(By.CLASS_NAME, "comments-comment-item")
            except Exception as e:
                # If window is closed, find_elements will throw a connection error
                if "Connection aborted" in str(e) or "forcibly closed" in str(e) or "invalid session" in str(e):
                    raise WebDriverException("Browser Closed") # Raise to outer block
                else:
                    comments = [] 

            for comment_node in comments:
                try:
                    # 1. Extract Text
                    text_elems = comment_node.find_elements(By.XPATH, ".//span[@dir='ltr']")
                    if not text_elems: continue
                    comment_text = text_elems[0].text.strip()
                    
                    # 2. Extract Author Name
                    author = "Unknown"
                    profile_link = ""
                    try:
                        # Try method A: The standard actor link
                        author_elem = comment_node.find_element(By.CSS_SELECTOR, "a.comments-post-meta__actor-link")
                        author = author_elem.text.split('\n')[0].strip()
                        profile_link = author_elem.get_attribute('href')
                    except:
                        try:
                            # Try method B: Sometimes it's just a span class
                            author_elem = comment_node.find_element(By.CSS_SELECTOR, "span.comments-post-meta__name-text")
                            author = author_elem.text.strip()
                        except:
                            pass 

                    # 3. Create Unique ID
                    unique_id = f"{author[:15]}_{comment_text[:20]}"

                    if unique_id not in seen_comments and comment_text:
                        sentiment = categorize_sentiment(sia, comment_text)
                        
                        # 4. Filter Logic
                        if "ALL" in target_categories or sentiment in target_categories:
                            seen_comments.add(unique_id)
                            
                            scraped_data.append({
                                "Author": author,
                                "Sentiment": sentiment,
                                "Comment": comment_text,
                                "Profile Link": profile_link,
                                "Date Scraped": time.strftime("%Y-%m-%d %H:%M:%S")
                            })
                            
                            # Console Output
                            prefix = "[+]" if sentiment in ["Good", "Very Good"] else "[-]" if sentiment in ["Bad", "Worst"] else "[=]"
                            print(f"{prefix} {sentiment.upper()} | {author}: {comment_text[:50]}...")

                except Exception: continue

            # Scroll
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(2)
            sys.stdout.write(f"\rTotal Collected: {len(scraped_data)} | Scanning... (Press Ctrl+C to save)")
            sys.stdout.flush()

    except KeyboardInterrupt:
        print("\n\n!!! STOPPING SCRAPER (User Interrupt) !!!")
    except Exception as e:
        # Catch browser closing or connection loss
        if "Browser Closed" in str(e) or "Connection aborted" in str(e) or "forcibly closed" in str(e):
             print("\n\n⚠️ Browser window closed. Saving collected data...")
        else:
             print(f"\n\n❌ Unexpected error: {e}")

    # 6. Export
    if scraped_data:
        timestamp = int(time.time())
        filename = f"linkedin_comments_{timestamp}.xlsx"
        print(f"\n[5/5] Saving {len(scraped_data)} comments to '{filename}'...")
        try:
            # Reorder columns to put Author first
            df = pd.DataFrame(scraped_data)
            cols = ["Author", "Sentiment", "Comment", "Profile Link", "Date Scraped"]
            df = df[cols]
            
            df.to_excel(filename, index=False)
            print(f"✅ Success! File saved: {filename}")
        except Exception as e:
            print(f"❌ Error saving file: {e}")
    else:
        print("\n⚠️ No comments collected.")

    try:
        driver.quit()
    except:
        pass
    input("Press Enter to exit.")

if __name__ == "__main__":
    main()
