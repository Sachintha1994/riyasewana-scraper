import os
import requests
from bs4 import BeautifulSoup
import hashlib
from emailer import send_email

HEADERS = {"User-Agent": "Mozilla/5.0"}
SEEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'seen_ads.txt')

def parse_listing(li):
    try:
        title_tag = li.find("h2", class_="more").find("a")
        title = title_tag.get("title").strip()
        link = title_tag.get("href")
        full_link = link if link.startswith("http") else "https://riyasewana.com" + link

        boxtext = li.find("div", class_="boxtext")
        box_items = boxtext.find_all("div", class_="boxintxt")

        location, price, mileage, date = None, None, None, None

        for item in box_items:
            text = item.text.strip()
            if "Rs." in text:
                price = text
            elif "km" in text:
                mileage = text
            elif "-" in text and text.count("-") == 2:
                date = text
            elif location is None:
                location = text

        return {
            "title": title,
            "location": location,
            "price": price,
            "mileage": mileage,
            "date": date,
            "link": full_link
        }
    except Exception as e:
        print(f"[!] Error parsing ad: {e}")
        return None

def scrape_model(model_config, pages=1):
    url = model_config['url']
    title = model_config['title']
    email_to = model_config['email_to']
    print(f"[*] Scraping start {title}: {url} : {email_to}")

    seen = set()

    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, 'r') as f:
            seen = set(f.read().splitlines())
    else:
        print(f"[*] Seen file not found at {SEEN_FILE}, starting fresh.")

    all_ads = []
    for page in range(1, pages + 1):
        page_url = f"{url}?page={page}" if page > 1 else url
        print(f"[*] Fetching page {page}: {page_url}")
        res = requests.get(page_url, headers=HEADERS)
        if res.status_code != 200:
            print(f"[!] Failed to fetch {page_url}")
            continue

        soup = BeautifulSoup(res.text, "html.parser")
        listings = soup.find_all("li", class_="item")

        for li in listings:
            ad = parse_listing(li)
            if not ad:
                continue

            hash_input = title + ad['link'] + email_to
            ad_hash = hashlib.md5(hash_input.encode()).hexdigest()
            if ad_hash in seen:
                continue

            seen.add(ad_hash)
            all_ads.append(ad)

    with open(SEEN_FILE, 'w') as f:
        for h in seen:
            f.write(h + "\n")

    if all_ads:
        send_email(
            ads=all_ads,
            subject=title,
            to=email_to
        )
    else:
        print("[*] No new ads found.")
