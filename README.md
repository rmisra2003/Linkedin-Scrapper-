LinkedIn Sentiment Analyzer & Scraper 🚀

A robust Command Line Interface (CLI) tool that scrapes comments from LinkedIn posts in real-time, performs sentiment analysis using VADER, and exports the categorized data to Excel.

Perfect for: Market researchers, recruiters, and content creators who need to quickly gauge community reaction (positive vs. negative) to specific LinkedIn posts.

🌟 Key Features

Real-time Scraping: Continuously extracts comments from a live LinkedIn post while you watch.

Sentiment Intelligence: Automatically classifies comments into 5 distinct categories:

🟢 Very Good (High Praise)

🙂 Good (Positive)

😐 Neutral

Orange Bad (Negative)

🔴 Worst (Highly Critical)

Smart Filtering: Choose to scrape only the negative comments, only positive ones, or everything.

Instant Excel Export: Press Ctrl+C at any time to stop the scraper and instantly save collected data to an .xlsx file.

Dual Login Modes: Supports both automated terminal login and manual browser login (perfect for bypassing CAPTCHA/2FA).

🛠️ Tech Stack

Core: Python 3.x

Automation: Selenium WebDriver

NLP: NLTK (VADER Lexicon)

Data Handling: Pandas, OpenPyXL

Packaging: PyInstaller (Optional for .exe creation)

📂 Project Structure

linkedin-sentiment-analyzer/
├── linkedin_analyzer.py    # Main application script
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
└── output/                # Generated Excel files (created automatically)


📋 Prerequisites

Before running the tool, ensure you have the following:

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
The tool provides two methods to authenticate:

Option [1] Terminal Input: Type email/password in the CLI. The script attempts to auto-fill them.

Option [2] Manual Browser (Recommended): A Chrome window opens. You manually type your details. Use this if you have 2FA enabled or encounter a CAPTCHA.

Configuration

Post URL: Paste the full URL of the LinkedIn post you want to analyze.

Filter: Select the type of comments you want to keep (e.g., Press 3 for "Bad" comments).

Scraping & Exporting

The browser will navigate to the post and start scrolling/clicking "Load More".

Real-time results will appear in your terminal.

To Stop: Press Ctrl+C in the terminal. The script will immediately save a file named linkedin_comments_[timestamp].xlsx.

🧠 How Sentiment Logic Works

The tool uses the VADER (Valence Aware Dictionary and sEntiment Reasoner) lexicon from NLTK. It calculates a "Compound Score" ranging from -1 to 1.

Category

Compound Score Range

Logic

Very Good

Score ≥ 0.5

enthusiastic, high praise

Good

0.05 ≤ Score < 0.5

generally positive

Neutral

-0.05 < Score < 0.05

factual or indifferent

Bad

-0.5 < Score ≤ -0.05

critical, negative

Worst

Score ≤ -0.5

hostile, very critical

❓ Troubleshooting

Q: The browser closes immediately.
A: Ensure Google Chrome is installed. Also, try running pip install --upgrade webdriver-manager.

Q: I get a CAPTCHA during login.
A: Restart the script and choose Option 2 (Manual Login). Solve the CAPTCHA in the browser, then press Enter in the terminal to continue.

Q: It says "NoSuchElementException".
A: LinkedIn often changes their HTML structure (class names). This script tries to use generic tags, but if they push a major update, the selectors might need adjustment.

🔮 Roadmap

[ ] Add support for "Reposts" and "Articles".

[ ] Add a graphical dashboard using Streamlit.

[ ] Implement proxy support to avoid rate limiting.

[ ] Add headless mode (run without opening a visible browser window).

⚠️ Disclaimer

This tool is for educational and research purposes only.

LinkedIn's Terms of Service: Automated scraping may violate LinkedIn's User Agreement. Use this tool responsibly and at your own risk.

Rate Limiting: Excessive scraping may flag your account. We recommend using a secondary account for heavy testing.

📄 License

Distributed under the MIT License. See LICENSE for more information.

🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
