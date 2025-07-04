<p align="center">
  <h1 align="center">🕷️ Universal Selenium Web Scraper</h1>
  <p align="center">
    <strong>Configure once. Scrape anywhere.</strong><br />
    A modular, pluggable web scraper that works on any tabular site with zero code rewrites.
  </p>
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
</p>

<details>
<summary><strong>📚 Table of Contents</strong></summary>

- [🔧 Feature Highlights](#-feature-highlights)
  - [🧩 Modular and Reusable Scraper Architecture](#-modular-and-reusable-scraper-architecture)
  - [📄 Zero-Code Configuration for New Targets](#-zero-code-configuration-for-new-targets)
  - [💾 Flexible, Pluggable Storage System](#-flexible-pluggable-storage-system)
  - [🧠 Intelligent Record Deduplication and Merging](#-intelligent-record-deduplication-and-merging)
  - [⚙️ Headless Chrome Automation (Local or Cloud)](#️-headless-chrome-automation-local-or-cloud)
  - [☁️ AWS Lambda Compatible](#️-aws-lambda-compatible)
  - [🔌 Workflow-Friendly & Extensible](#-workflow-friendly--extensible)
- [⚙️ Setup Instructions](#️-setup-instructions)
- [🚀 Quick Start](#-quick-start)
- [📁 File Structure](#-file-structure)
- [📄 License](#-license)
- [❓ Quick FAQ](#-quick-faq)
- [✨ Credits](#-credits)

</details>

## 🔧 Feature Highlights

---

### 🧩 Modular and Reusable Scraper Architecture

This scraper is designed to work across any website with tabular or row-based data. The core logic (scraping, browser setup, storage) is fully decoupled. Just update a config dictionary — no rewrites required.

```python
CONFIG = {
  "url": "https://example.com/data",
  "row_css": "table.data tr",
  "column_map": {"name": 0, "price": 1},
  "key_fields": ["name"]
}
````

---

### 📄 Zero-Code Configuration for New Targets

Instead of writing parsing logic, just fill in:

* `url`: page to scrape
* `row_css`: selector for rows
* `column_map`: map of column names to indexes
* `key_fields`: defines uniqueness per row

```python
row_css = "div.card"
column_map = {
  "title": 0,
  "author": 1,
  "rating": 2
}
```

---

### 💾 Flexible, Pluggable Storage System

Save data anywhere. Built-in backends include:

* ✅ Local JSON files
* ☁️ AWS S3
* 🛠️ Easy to extend to SQL, Firebase, REST APIs, etc.

```python
from backends import LocalJSON, S3JSON

storage = LocalJSON("output.json")
# or
storage = S3JSON(bucket="my-bucket", key="results.json")
```

---

### 🧠 Intelligent Record Deduplication and Merging

The scraper compares new rows with saved ones using your `key_fields`. It:

* Updates changed rows
* Skips exact duplicates
* Adds newly discovered rows

```python
merge_unique(existing_data, new_data, key_fields=["name", "location"])
```

---

### ⚙️ Headless Chrome Automation (Local or Cloud)

Supports all environments with preconfigured options:

* Local dev
* Docker or CI pipelines
* AWS Lambda (with headless Chromium)

```python
opts.add_argument("--headless=new")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")
```

---

### ☁️ AWS Lambda Compatible

Drop this into Lambda for scheduled scraping:

* Built-in `lambda_handler()`
* S3-compatible storage
* Lightweight Chrome configuration

```python
def lambda_handler(event, context):
    run_scraper(CONFIG, S3JSON("my-bucket"))
```

---

### 🔌 Workflow-Friendly & Extensible

Integrates easily into:

* Airflow, Prefect, Dagster
* Cron jobs or GitHub Actions
* Flask/FastAPI backends or CLI tools

```python
from universal_scraper import run_scraper
run_scraper(CONFIG, LocalJSON("results.json"))
```

You can also override internals like:

```python
def custom_merge(existing, new):
    return existing + [x for x in new if x["flagged"] == "yes"]
```

---

## ⚙️ Setup Instructions

---

### 1. Install Python dependencies

```bash
pip install selenium boto3
```

> *(Optionally add `chromedriver-autoinstaller` to auto-manage drivers)*

---

### 2. Install Chrome & ChromeDriver

---

#### macOS

```bash
brew install --cask google-chrome
brew install chromedriver
```

---

#### Ubuntu / Debian

```bash
sudo apt update
sudo apt install -y chromium-browser chromium-chromedriver
```

---

#### Windows

1. Get Chrome version: `chrome://version`
2. Download matching driver: [chromedriver.chromium.org](https://chromedriver.chromium.org/downloads)
3. Add to PATH

---

#### Auto Installer (Local Dev Only)

```bash
pip install chromedriver-autoinstaller
```

```python
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
```

---

## 🚀 Quick Start

---

### 1. Configure your target

```python
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
```

---

### 2. Run the scraper

```bash
python universal_scraper.py
```

---

## 📁 File Structure

---

```bash
universal_scraper.py     # Main scraper logic and Lambda handler
README.md                # You're here
requirements.txt         # Dependencies
```

---

## 📄 License

---

MIT License — free to use, modify, and distribute.


---

## ❓ Quick FAQ

<details>
<summary><strong>❓ Quick FAQ (Troubleshooting Cheatsheet)</strong></summary>

---

### 1. `ModuleNotFoundError: No module named 'backends'`
**Cause:** The example code assumes a `backends.py` file exists.

**Fix:** Either define `LocalJSON` inline in your script:
```python
class LocalJSON:
    def __init__(self, path="results.json"):
        self.path = path

    def load(self):
        if not os.path.exists(self.path):
            return []
        with open(self.path, "r") as f:
            return json.load(f)

    def save(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)
````

Or create a new `backends.py` file containing that class and import it with:

```python
from backends import LocalJSON
```

---

### 2. `TypeError: Options.binary_location must be a string`

**Cause:** You're assigning `None` to `opts.binary_location` when not running in AWS Lambda.

**Fix:**

```python
if chrome_binary:
    opts.binary_location = chrome_binary
```

---

### 3. Chrome / ChromeDriver version mismatch

**Error:**
`This version of ChromeDriver only supports Chrome version X`

**Fix:** Auto-install the matching ChromeDriver at runtime:

```bash
pip install chromedriver-autoinstaller
```

Then add this to your script before launching the driver:

```python
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
```

---

### 4. `WebDriverException: cannot find Chrome binary`

**Fixes:**

* ✅ Local: Install Google Chrome.
* ✅ CI/Docker: Use an image that includes Chrome.
* ✅ AWS Lambda: Add a headless Chromium layer and set:

```python
chrome_binary = "/opt/bin/chromium"
```

---

### 5. Selector finds 0 rows

**Fix:**

* Open DevTools and test:

```js
document.querySelectorAll("your_row_css").length
```

* Confirm content isn't loaded asynchronously (JS delay).
* Use `WebDriverWait()` for dynamic content to load:

```python
WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, row_css))
)
```

---

### 6. Running on AWS Lambda

**Steps:**

1. Zip your code + dependencies
2. Attach a headless Chromium Lambda Layer
3. Set handler:

```python
universal_scraper.lambda_handler
```

4. Use `S3JSON("your-bucket")` for storage

---

### 7. My output JSON is empty

**Check:**

* Your CSS selector is valid
* You’re targeting the correct elements
* `key_fields` aren’t incorrectly filtering all rows
* Clear your local JSON file and rerun for a clean test

</details>

---

## ✨ Credits

---

Built by [@mattcsnyder](https://github.com/mattcsnyder) for developers who want powerful scraping tools without rewriting boilerplate.
Just drop in your config, and you're good to go.
