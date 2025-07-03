"""
universal_scraper.py
--------------------
A plug-and-play Selenium scraper for any tabular (or row-based) web page.

Quick-start
-----------
1.  Fill in a CONFIG dict (see bottom of file or pass one at runtime).
2.  Choose / implement a StorageBackend (JSON, S3, SQL, etc.).
3.  Call run_scraper(CONFIG, storage_backend).

The core library code below never needs editing when you move to a
different site—only the CONFIG changes.
"""

import json, os, logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ───────────────────────────── Logging ─────────────────────────────
log = logging.getLogger("universal_scraper")
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())

# ──────────────── Driver factory (works local & AWS Lambda) ─────────
def create_driver(headless: bool = True) -> webdriver.Chrome:
    in_lambda = "LAMBDA_TASK_ROOT" in os.environ
    chrome_binary = "/opt/bin/chromium" if in_lambda else None  # let Chrome choose locally

    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.binary_location = chrome_binary

    return webdriver.Chrome(service=Service(), options=opts)

# ─────────────── Storage backend plug-ins (choose / extend) ─────────
class StorageBackend(ABC):
    @abstractmethod
    def load(self) -> List[Dict[str, Any]]:
        ...
    @abstractmethod
    def save(self, data: List[Dict[str, Any]]) -> None:
        ...

class LocalJSON(StorageBackend):
    """Simple local file storage."""
    def __init__(self, path: str = "scrape_results.json"):
        self.path = path
    def load(self):
        if not os.path.exists(self.path):
            return []
        with open(self.path) as f:
            return json.load(f)
    def save(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

# ───────────────────────── Core scraping helper ────────────────────
def scrape_rows(driver: webdriver.Chrome,
                url: str,
                row_css: str,
                column_map: Dict[str, int],
                wait_sec: int = 30) -> List[Dict[str, str]]:
    """Navigate to *url*, wait for rows matching *row_css*, return parsed data.

    column_map = {"field_name": column_index_in_row, ...}
    """
    log.info("Loading %s", url)
    driver.get(url)
    WebDriverWait(driver, wait_sec).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, row_css))
    )
    rows = driver.find_elements(By.CSS_SELECTOR, row_css)

    data: List[Dict[str, str]] = []
    for r in rows:
        cells = r.find_elements(By.TAG_NAME, "td")
        if len(cells) < max(column_map.values()) + 1:
            continue
        record = {field: cells[idx].text.strip() for field, idx in column_map.items()}
        data.append(record)
    log.info("Extracted %d rows", len(data))
    return data

# ────────────────────────── Data merge helper ──────────────────────
def merge_unique(old: List[Dict[str, Any]],
                 new: List[Dict[str, Any]],
                 key_fields: List[str]) -> List[Dict[str, Any]]:
    """Return union of old+new where *key_fields* identify a unique row."""
    index = {tuple(o[k] for k in key_fields): i for i, o in enumerate(old)}
    for item in new:
        k = tuple(item[k] for k in key_fields)
        if k in index:
            old[index[k]] = item          # overwrite old copy
        else:
            old.append(item)
    return old

# ─────────────────────────── Main worker ───────────────────────────
def run_scraper(config: Dict[str, Any], storage: StorageBackend) -> None:
    drv = create_driver()
    try:
        fresh = scrape_rows(drv,
                            url=config["url"],
                            row_css=config["row_css"],
                            column_map=config["column_map"])
        existing = storage.load()
        merged   = merge_unique(existing, fresh, config["key_fields"])
        storage.save(merged)
        log.info("Saved %d total records", len(merged))
    finally:
        drv.quit()

# ─────────────────────────── Example stub ──────────────────────────
if __name__ == "__main__":
    CONFIG = {
        # Fill with *your* site details — nothing here is tied to any brand
        "url": "https://example.com/table-page",
        "row_css": "table#main tbody tr",
        "column_map": {          # readable_name : <td> index
            "id": 0,
            "title": 1,
            "price": 2,
            "updated": 3,
        },
        "key_fields": ["id"],    # identifies a unique item
    }

    storage_backend = LocalJSON("example_results.json")
    run_scraper(CONFIG, storage_backend)

# ───────────────────────── AWS Lambda wrapper ──────────────────────
def lambda_handler(event, context):
    """
    Deploy this file to Lambda along with a headless Chrome layer.
    Supply CONFIG via env-vars, Secrets Manager, SSM, or code import.
    """
    CONFIG = {...}                 # ← provide the same structure
    storage = LocalJSON("/tmp/results.json")  # or custom backend
    run_scraper(CONFIG, storage)
    return {"statusCode": 200,
            "body": f"Scrape completed @ {datetime.utcnow().isoformat()}Z"}