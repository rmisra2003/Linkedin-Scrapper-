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

# --- CONFIGURATION ---
# Download VADER lexicon for sentiment analysis if not present
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    print("Downloading VADER lexicon...")
    nltk.download('vader_lexicon')

def categorize_sentiment(sia, text):
    """
    Analyzes text using VADER and returns a specific category.
    Returns: 'Very Good', 'Good', 'Neutral', 'Bad', or 'Worst'
    """
    if not text:
        return "Neutral"
        
    scores = sia.polarity_scores(text)
    compound = scores['compound']
    
    # Custom thresholds for sentiment categorization
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

def attempt_terminal_login(driver):
    """
    Takes credentials from the terminal and attempts to auto-fill them in the browser.
    """
    print("\n--- Terminal Login Credentials ---")
    email = input("  -> Email: ").strip()
    password = getpass.getpass("  -> Password (hidden): ").strip()
    
    print("\n  -> Attempting to log in...")
    
    try:
        # Wait for username field to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        
        # Enter Email
        email_elem = driver.find_element(By.ID, "username")
        email_elem.clear()
        email_elem.send_keys(email)
        
        # Enter Password
        pass_elem = driver.find_element(By.ID, "password")
        pass_elem.clear()
        pass_elem.send_keys(password)
        pass_elem.send_keys(Keys.RETURN)
        
        print("  -> Credentials submitted.")
        
        # Simple check to see if URL changes (indicating successful login or 2FA step)
        time.sleep(5)
        if "feed" in driver.current_url or "checkpoint" not in driver.current_url:
            print("  -> Login flow processing...")
        else:
            print("  -> ! CAPTCHA OR 2FA DETECTED !")
            
    except Exception as e:
        print(f"  -> Automated login failed: {e}")
        print("  -> Please finish logging in manually in the browser.")

def main():
    print("========================================")
    print("   LINKEDIN COMMENT SENTIMENT CLI")
    print("========================================")

    # 1. Setup Driver
    print("\n[1/5] Launching Browser...")
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")  # Suppress generic logs
    # options.add_argument("--headless")   # Uncomment to run without window (not recommended for login)
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception as e:
        print(f"Error launching Chrome: {e}")
        return

    # 2. Login Phase
    driver.get("https://www.linkedin.com/login")
    
    print("\n[2/5] Login Method:")
    print("     [1] Enter Credentials Here (Terminal)")
    print("     [2] Log in Manually in Browser (Safer/Bypasses CAPTCHA)")
    login_choice = input("  -> Choose (1/2): ").strip()
    
    if login_choice == '1':
        attempt_terminal_login(driver)
        input("\n  -> Check Browser: If Login/CAPTCHA is done, PRESS ENTER here to continue...")
    else:
        print("\n  -> ACTION REQUIRED: Please Log in to LinkedIn in the opened Chrome window.")
        input("  -> Once you are logged in, PRESS ENTER here to continue...")

    # 3. User Inputs
    print("\n[3/5] Configuration:")
    post_url = input("  -> Paste the LinkedIn Post URL here: ").strip()
    
    print("\n  -> Which comments do you want to keep?")
    print("     [1] Very Good  (High Praise)")
    print("     [2] Good       (Positive)")
    print("     [3] Bad        (Negative)")
    print("     [4] Worst      (Highly Critical)")
    print("     [5] ALL        (Keep Everything)")
    
    choice = input("  -> Enter choice (1-5): ").strip()
    
    target_category = "ALL"
    if choice == '1': target_category = "Very Good"
    elif choice == '2': target_category = "Good"
    elif choice == '3': target_category = "Bad"
    elif choice == '4': target_category = "Worst"

    # 4. Navigation & Scraping Setup
    print(f"\n[4/5] Navigating to post and starting scraper for '{target_category}' comments...")
    print("---------------------------------------------------------------")
    print("  !!! PRESS CTRL+C AT ANY TIME TO STOP AND SAVE TO EXCEL !!!")
    print("---------------------------------------------------------------")
    
    try:
        driver.get(post_url)
    except Exception as e:
        print(f"Invalid URL: {e}")
        driver.quit()
        return

    sia = SentimentIntensityAnalyzer()
    scraped_data = []
    seen_comments = set()
    
    # 5. The Scraping Loop
    try:
        while True:
            # A. Try to click 'Load more comments' buttons
            try:
                load_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'comments-comments-list__load-more-comments-button')]")
                for btn in load_buttons:
                    if btn.is_displayed():
                        driver.execute_script("arguments[0].click();", btn)
                        time.sleep(1)
            except:
                pass

            # B. Find all comment articles
            comments = driver.find_elements(By.TAG_NAME, "article")
            
            new_in_batch = 0
            
            for comment_node in comments:
                try:
                    # Extract Text
                    # LinkedIn text is usually in a span with dir='ltr'
                    text_elements = comment_node.find_elements(By.XPATH, ".//span[@dir='ltr']")
                    if not text_elements: continue
                    
                    comment_text = text_elements[0].text.strip()
                    
                    # Extract Author Name
                    try:
                        author_elem = comment_node.find_element(By.CSS_SELECTOR, "a.comments-post-meta__actor-link")
                        author = author_elem.text.split('\n')[0]
                        profile_link = author_elem.get_attribute('href')
                    except:
                        author = "Unknown"
                        profile_link = ""

                    # Generate a simple ID to prevent duplicates
                    unique_id = f"{author[:15]}_{comment_text[:20]}"

                    if unique_id not in seen_comments and comment_text:
                        # Analyze Sentiment
                        sentiment = categorize_sentiment(sia, comment_text)
                        
                        # Filter Logic: Only add if it matches user choice or user selected ALL
                        if target_category == "ALL" or sentiment == target_category:
                            seen_comments.add(unique_id)
                            
                            row = {
                                "Author": author,
                                "Sentiment": sentiment,
                                "Comment": comment_text,
                                "Profile": profile_link,
                                "Date Scraped": time.strftime("%Y-%m-%d %H:%M:%S")
                            }
                            scraped_data.append(row)
                            new_in_batch += 1
                            
                            # Real-time console output
                            # Print colored output based on sentiment for better visibility
                            prefix = "[+]" if sentiment in ["Good", "Very Good"] else "[-]" if sentiment in ["Bad", "Worst"] else "[=]"
                            print(f"{prefix} {sentiment.upper()} | {author}: {comment_text[:50]}...")

                except Exception:
                    continue

            # C. Scroll down to trigger lazy loading
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(2) # Wait for network load
            
            # Show aliveness spinner on same line
            sys.stdout.write(f"\rTotal Collected: {len(scraped_data)} | Scanning... (Press Ctrl+C to save)")
            sys.stdout.flush()

    except KeyboardInterrupt:
        print("\n\n!!! STOPPING SCRAPER (User Interrupt) !!!")

    # 6. Export Data
    if scraped_data:
        timestamp = int(time.time())
        filename = f"linkedin_comments_{target_category.replace(' ', '_')}_{timestamp}.xlsx"
        print(f"\n[5/5] Saving {len(scraped_data)} comments to '{filename}'...")
        try:
            df = pd.DataFrame(scraped_data)
            # Reorder columns for better Excel readability
            cols = ["Sentiment", "Author", "Comment", "Profile", "Date Scraped"]
            df = df[cols]
            
            df.to_excel(filename, index=False)
            print(f"✅ Success! File saved: {filename}")
        except Exception as e:
            print(f"❌ Error saving file: {e}")
    else:
        print("\n⚠️ No comments collected to save.")

    print("Closing browser...")
    driver.quit()
    input("Press Enter to exit.")

if __name__ == "__main__":
    main()