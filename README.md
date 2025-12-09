Here is the **fully formatted, clean, GitHub-ready README** using proper Markdown headers (`#`, `##`, `###`), tables, code blocks, and bullet styling — **just copy–paste into README.md**:

---

# 🚀 LinkedIn Sentiment Analyzer & Scraper

A powerful **Command Line Interface (CLI)** tool that scrapes comments from LinkedIn posts in real-time, performs sentiment analysis using **VADER**, and exports the categorized results into an Excel file.

Perfect for **market researchers**, **recruiters**, **growth analysts**, and **content creators** who need to quickly measure audience sentiment on any LinkedIn post.

---

## 🌟 Features

### 🔄 Real-time Scraping

Continuously extracts comments from a LinkedIn post while displaying results live in your terminal.

### 🧠 Sentiment Intelligence

Automatically classifies each comment into **5 sentiment categories**:

| Category         | Description               |
| ---------------- | ------------------------- |
| 🟢 **Very Good** | Highly positive, praising |
| 🙂 **Good**      | Generally positive        |
| 😐 **Neutral**   | Factual or indifferent    |
| 🟠 **Bad**       | Negative or critical      |
| 🔴 **Worst**     | Highly negative, hostile  |

### 🎯 Smart Filtering

Choose to extract:

* Only **negative** comments
* Only **positive** comments
* **All** comments

### 📊 Instant Excel Export

Press **Ctrl + C** anytime → all collected comments are instantly saved to an `.xlsx` file.

### 🔐 Dual Login Modes

* **Option 1 — Terminal Login**: Enter email/password and the script attempts to auto-fill.
* **Option 2 — Manual Browser Login (recommended)**: A Chrome window opens for you to manually log in (bypasses 2FA & CAPTCHA).

---

## 🛠️ Tech Stack

* **Python 3.x**
* **Selenium WebDriver**
* **NLTK (VADER)**
* **Pandas**
* **OpenPyXL**
* **PyInstaller** (optional)

---

## 📂 Project Structure

```
linkedin-sentiment-analyzer/
├── linkedin_analyzer.py     # Main application script
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
└── output/                  # Excel files generated during export
```

---

## 📋 Prerequisites

Before running the tool, ensure you have:

* **Google Chrome** installed
* **Python 3.x** installed (with “Add to PATH” enabled)

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/linkedin-sentiment-analyzer.git
cd linkedin-sentiment-analyzer
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, use:

```bash
pip install selenium pandas nltk openpyxl webdriver-manager
```

---

## 🚀 How to Use

### 1️⃣ Run the Script

```bash
python linkedin_analyzer.py
```

---

### 2️⃣ Login Phase

You will see:

#### **Option [1] — Terminal Input**

Enter email/password in CLI → script auto-fills login.

#### **Option [2] — Manual Browser Login (Recommended)**

A Chrome window opens → login manually, solve CAPTCHA or 2FA.
Once done, return to terminal and press **Enter**.

---

### 3️⃣ Provide Configuration

You will be prompted to enter:

* ✔️ **LinkedIn post URL**
* ✔️ **Filter type** (All / Positive / Negative categories)

---

### 4️⃣ Scraping & Export

* The tool loads all comments by scrolling and clicking “Load more”.
* Sentiment classification appears live in your terminal.
* Press **Ctrl + C** at any point to stop scraping.
* Tool saves an Excel file automatically:

```
linkedin_comments_YYYY-MM-DD_HH-MM-SS.xlsx
```

Stored inside the `output/` folder.

---

## 🧠 How Sentiment Logic Works (VADER)

VADER assigns a **compound score** between `-1` and `1`.

| Category      | Score Range     | Meaning         |
| ------------- | --------------- | --------------- |
| **Very Good** | `≥ 0.5`         | Highly positive |
| **Good**      | `0.05 to 0.5`   | Positive        |
| **Neutral**   | `-0.05 to 0.05` | Neutral         |
| **Bad**       | `-0.5 to -0.05` | Negative        |
| **Worst**     | `≤ -0.5`        | Highly negative |

---

## ❓ Troubleshooting

**Q: Browser closes immediately**
A: Ensure Chrome is installed and run:

```bash
pip install --upgrade webdriver-manager
```

**Q: I get a CAPTCHA**
A: Restart the tool → choose **Option 2 (Manual Login)**.

**Q: NoSuchElementException errors**
A: LinkedIn frequently updates their HTML. Update class selectors accordingly.

---

## 🔮 Roadmap

* [ ] Support for Reposts and Articles
* [ ] Add a Streamlit GUI
* [ ] Proxy support to avoid rate limiting
* [ ] Headless mode

---

## ⚠️ Disclaimer

This tool is meant for **educational and research purposes only**.

* Scraping LinkedIn may violate their **Terms of Service**.
* Heavy use may result in **account restrictions**.
* Use a **secondary account** for testing.

---

## 📄 License

Distributed under the **MIT License**.

---

## 🤝 Contributing

Contributions, issues, and pull requests are welcome!

