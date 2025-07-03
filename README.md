<p align="center">
  <a href="https://github.com/mattcsnyder" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-@mattcsnyder-black?logo=github&style=for-the-badge" />
  </a>
  <a href="https://www.instagram.com/fullstackwithmatt" target="_blank">
    <img src="https://img.shields.io/badge/Instagram-@fullstackwithmatt-E4405F?logo=instagram&logoColor=white&style=for-the-badge" />
  </a>
  <a href="https://www.threads.com/@fullstackwithmatt" target="_blank">
    <img src="https://img.shields.io/badge/Threads-@fullstackwithmatt-000000?logo=threads&logoColor=white&style=for-the-badge" />
  </a>
</p>

# Universal-Scraper
A plug-and-play Selenium scraper for any tabular (or row-based) web page.

# 🕷️ Universal Selenium Web Scraper

A plug-and-play, highly configurable Python scraper built with Selenium. Extract tabular or row-based data from any website by simply editing a configuration dictionary — no code rewrites required.

---

## 🔧 Feature Highlights

---

---
### 🧩 Modular and Reusable Scraper Architecture  
This scraper is designed to be reused across any website with tabular or row-based data structures. The scraping logic, browser setup, and storage mechanisms are fully decoupled, making the core logic universally portable with zero rewrites required. Just update the `CONFIG` dictionary — no need to touch the rest of the codebase.
---

```python
CONFIG = {
  "url": "https://example.com/data",
  "row_css": "table.data tr",
  "column_map": {"name": 0, "price": 1},
  "key_fields": ["name"]
}
```

---
### 📄 Zero-Code Configuration for New Targets
---

Instead of rewriting parsing logic, define what you want to extract using a single CONFIG object:
	•	url: the page to scrape
	•	row_css: the CSS selector for rows
	•	column_map: mapping of field names to <td> indices
	•	key_fields: which columns uniquely identify a record

row_css = "div.card"
column_map = {
  "title": 0,
  "author": 1,
  "rating": 2
}

---
💾 Flexible, Pluggable Storage System
---

The scraper supports a pluggable storage backend interface so data can be saved anywhere:
	•	✅ Local JSON files (default)
	•	☁️ S3 buckets for serverless/cloud deployments
	•	🛠️ Easily extendable to SQL, Firebase, Airtable, Google Sheets, etc.

from backends import LocalJSON, S3JSON

storage = LocalJSON("output.json")
# or
storage = S3JSON(bucket="my-bucket", key="results.json")

---
🧠 Intelligent Record Deduplication and Merging
---

Instead of blindly saving new data, the scraper compares incoming rows to previously saved data using your defined key_fields. It:
	•	Updates changed rows
	•	Adds new rows
	•	Skips duplicates

merge_unique(existing_data, new_data, key_fields=["name", "location"])

---
⚙️ Headless Chrome Automation (Cloud or Local)
---

Works out of the box in:
	•	Local dev environments (via ChromeDriver)
	•	AWS Lambda (with chromium headless layer)
	•	CI/CD pipelines using Docker or GitHub Actions

Chrome is preconfigured for headless use:

opts.add_argument("--headless=new")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")

---
☁️ AWS Lambda Compatible
---

Deploy the scraper as-is to AWS Lambda for automated or scheduled scraping tasks:
	•	Built-in lambda_handler entry point
	•	Chrome and driver detection for Lambda environments
	•	Cloud storage support with S3

def lambda_handler(event, context):
    run_scraper(CONFIG, S3JSON("my-bucket"))

---
🔌 Easy Integration with Workflows and Pipelines
---

Plug into any of your workflows:
	•	Airflow, Prefect, or Dagster
	•	GitHub Actions or cron
	•	Flask, FastAPI, or any CLI script

from universal_scraper import run_scraper

run_scraper(CONFIG, LocalJSON("results.json"))

---
🧪 Designed for Extensibility
---

You can override or extend any part of the pipeline:
	•	Customize scrape_rows() to parse non-table layouts
	•	Extend merge_unique() to enforce business logic
	•	Add post-processing like alerts or data uploads

def custom_merge(existing, new):
    # Example: Only add new flagged items
    return existing + [x for x in new if x['flagged'] == "yes"]

---
⚙️ Quick Setup
---

1. Install Python dependencies

pip install selenium boto3  # Add chromedriver-autoinstaller if needed


2. Install Chrome and ChromeDriver

🔧 macOS

brew install --cask google-chrome
brew install chromedriver

🐧 Ubuntu / Debian

sudo apt-get update
sudo apt-get install -y chromium-browser chromium-chromedriver

🪟 Windows
	1.	Find your Chrome version: chrome://version
	2.	Download matching ChromeDriver
	3.	Add the unzipped folder to your system PATH

💡 Auto Installer (Dev only)

pip install chromedriver-autoinstaller

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

---
🚀 Quick Start
---

Update your config in universal_scraper.py:

CONFIG = {
  "url": "https://example.com/data",
  "row_css": "table tr",
  "column_map": {
    "id": 0,
    "title": 1,
    "price": 2
  },
  "key_fields": ["id"]
}

Then run:

python universal_scraper.py

---
📁 File Structure
---

universal_scraper.py     # Main logic and Lambda handler
README.md                # You're here
requirements.txt         # Pip dependencies

---
📄 License
---

MIT License — free to use, modify, and distribute.

---
✨ Credits
---

Created for developers who are tired of rewriting the same scraper every week.
Drop in your config, and you’re scraping in minutes.

Let me know if you want:
- A **template repo** link
- A **Dockerfile**
- Sample **GitHub Actions workflow**
- Styling for a **landing page version** with visuals

Ready to ship as-is!