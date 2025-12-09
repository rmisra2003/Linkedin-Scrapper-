LinkedIn Sentiment Analyzer & Scraper 🚀

A robust Python CLI tool that scrapes comments from LinkedIn posts in real-time, performs sentiment analysis (VADER), and exports the data to Excel.

Designed for market researchers, recruiters, and content creators who need to quickly gauge community reaction to specific LinkedIn posts.

🌟 Features

Real-time Scraping: Continuously extracts comments from a live LinkedIn post.

Sentiment Analysis: Automatically classifies comments into 5 categories:

Very Good (High Praise)

Good (Positive)

Neutral

Bad (Negative)

Worst (Highly Critical)

Smart Filtering: Choose to scrape only the negative comments, only positive ones, or everything.

Excel Export: Press Ctrl+C at any time to instantly save collected data to an .xlsx file.

Dual Login Modes: Supports both automated terminal login and manual browser login (to bypass CAPTCHA/2FA).

🛠️ Tech Stack

Python 3.x

Selenium: For browser automation and scraping dynamic content.

NLTK (VADER): For natural language processing and sentiment scoring.

Pandas: For data structuring and Excel export.

Tkinter (Optional): Used in previous versions, currently pure CLI.

📋 Prerequisites

Google Chrome: Must be installed on your machine.

Python: Download Python (Ensure "Add to PATH" is checked during installation).

⚙️ Installation

Clone the Repository

git clone [https://github.com/yourusername/linkedin-sentiment-analyzer.git](https://github.com/yourusername/linkedin-sentiment-analyzer.git)
cd linkedin-sentiment-analyzer


Install Dependencies

pip install -r requirements.txt


If you don't have a requirements file yet, run:

pip install selenium pandas nltk openpyxl webdriver-manager


🚀 How to Use

Run the Script

python linkedin_analyzer.py


Login Phase
The tool will ask how you want to log in:

[1] Enter Credentials Here: Type email/password in the terminal. The script attempts to auto-fill them.

[2] Log in Manually: A Chrome window opens. You manually type your details. This is recommended if you have 2FA enabled or hit a CAPTCHA.

Configuration

Post URL: Paste the full URL of the LinkedIn post you want to analyze.

Filter: Select the type of comments you want to keep (e.g., Press 3 for "Bad" comments).

Scraping & Exporting

The browser will navigate to the post and start scrolling/clicking "Load More".

Real-time results will appear in your terminal.

To Stop: Press Ctrl+C in the terminal. The script will immediately save a file named linkedin_comments_[timestamp].xlsx in the project folder.

🧠 How Sentiment Logic Works

The tool uses the VADER (Valence Aware Dictionary and sEntiment Reasoner) lexicon from NLTK. It calculates a "Compound Score" ranging from -1 to 1.

Category

Compound Score Range

Very Good

Score ≥ 0.5

Good

0.05 ≤ Score < 0.5

Neutral

-0.05 < Score < 0.05

Bad

-0.5 < Score ≤ -0.05

Worst

Score ≤ -0.5

⚠️ Disclaimer

This tool is for educational and research purposes only.

LinkedIn's Terms of Service: Automated scraping may violate LinkedIn's User Agreement. Use this tool responsibly and at your own risk.

Rate Limiting: Excessive scraping may flag your account.

🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
