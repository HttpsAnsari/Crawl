import requests
import time
import random
from datetime import datetime

# ===================== CONFIG =====================
SEARCH_STRING = "12VVRNPi4SJqUTsp6"                    # CHANGE THIS
START_PAGE = 36893488147419103233
END_PAGE = 73786976294838206464                        # You can set 2 million, no problem
CHECKPOINT_FILE = "last_checked_page.txt"
OUTPUT_FILE = "found_results.txt"
# ==================================================

def load_progress():
    try:
        with open(CHECKPOINT_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return START_PAGE

def save_progress(page):
    with open(CHECKPOINT_FILE, "w") as f:
        f.write(str(page))

def log_found(page, url, context):
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | PAGE {page} | {url}\n")
        f.write(f"   → {context}\n\n")

# ===================== MAIN =====================
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

current_page = load_progress()
print(f"Starting from page {current_page} → {END_PAGE}")
print(f"Looking for: '{SEARCH_STRING}'")
print("Progress auto-saved. You can close and resume anytime!\n")

found_count = 0

for page in range(current_page, END_PAGE + 1):
    url = f"https://lbc.cryptoguru.org/dio/{page}"
    
    for attempt in range(5):  # retry up to 5 times
        try:
            r = requests.get(url, headers=headers, timeout=20)
            
            if r.status_code == 503 or r.status_code == 429:
                print(f"  [Page {page}] 503 → sleeping 10s...")
                time.sleep(10)
                continue
                
            if r.status_code != 200:
                print(f"  [Page {page}] HTTP {r.status_code} → retrying...")
                time.sleep(3)
                continue
                
            # Success!
            if SEARCH_STRING.lower() in r.text.lower():
                idx = r.text.lower().find(SEARCH_STRING.lower())
                snippet = r.text[idx-120:idx+120].replace("\n", " ")
                print(f"\nFOUND #{found_count+1} → PAGE {page}")
                print(f"   {snippet}...\n")
                log_found(page, url, snippet)
                found_count += 1
            
            break  # exit retry loop
            
        except Exception as e:
            if attempt == 4:
                print(f"  [Page {page}] Failed after 5 tries")
            else:
                time.sleep(5)
    
    # Show live progress
    print(f"Checked page {page} | Found so far: {found_count}", end="\r")
    
    # Save progress every 100 pages
    if page % 100 == 0:
        save_progress(page)
    
    # Be gentle to the server (0.6–1.2 seconds between requests)
    time.sleep(0.6 + random.random() * 0.6)

# Final save
save_progress(END_PAGE + 1)
print(f"\n\nFinished! Scanned up to page {END_PAGE}")
print(f"Total found: {found_count} → saved in {OUTPUT_FILE}")