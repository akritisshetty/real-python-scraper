"""Scrape article cards from the realpython.com homepage (RSS feed as fallback)."""
import datetime as dt
import re
import time
from urllib.parse import urljoin

import cloudscraper
import feedparser
from bs4 import BeautifulSoup

HOME_URL = "https://realpython.com/"
FEED_URL = "https://realpython.com/feed"
DATE_RE = re.compile(r"\w{3} \d{1,2}, \d{4}")
ATTEMPTS = 5
BACKOFF = 5


def _fetch(url):
    for i in range(ATTEMPTS):
        try:
            r = cloudscraper.create_scraper().get(url, timeout=30)
            print(f"fetch {url} attempt {i + 1}/{ATTEMPTS} -> {r.status_code}")
            if r.status_code == 200:
                return r.text
        except Exception as e:
            print(f"fetch {url} attempt {i + 1}/{ATTEMPTS} -> error {e}")
        if i < ATTEMPTS - 1:
            time.sleep(BACKOFF * (i + 1))
    raise RuntimeError(f"failed after {ATTEMPTS} attempts: {url}")


def _parse_date(raw):
    m = DATE_RE.search(raw)
    return dt.datetime.strptime(m.group(0), "%b %d, %Y").date() if m else None


def parse_home(html):
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for card in soup.select("div.card.border-0"):
        title = card.select_one("h2.card-title")
        if not title or title.parent.name != "a":
            continue
        desc = card.select_one("p.my-1")
        date_el = card.select_one(".text-muted span.me-2")
        rows.append({
            "title": title.get_text(strip=True),
            "url": urljoin(HOME_URL, title.parent["href"]),
            "description": desc.get_text(strip=True) if desc else None,
            "published_at": _parse_date(date_el.get_text(strip=True)) if date_el else None,
            "categories": [b.get_text(strip=True) for b in card.select("a.badge")],
        })
    return rows


def parse_feed(xml):
    feed = feedparser.parse(xml)
    rows = []
    for e in feed.entries:
        pub = e.get("published_parsed") or e.get("updated_parsed")
        rows.append({
            "title": e.get("title"),
            "url": e.get("link"),
            "description": re.sub(r"<[^>]+>", "", e.get("summary", "")).strip(),
            "published_at": dt.datetime(*pub[:3]).date() if pub else None,
            "categories": [t.get("term") for t in e.get("tags", [])],
        })
    return rows


def scrape():
    try:
        rows = parse_home(_fetch(HOME_URL))
        if rows:
            return rows
        print("homepage gave no cards, falling back to RSS feed")
    except Exception:
        print("homepage blocked, falling back to RSS feed")
    return parse_feed(_fetch(FEED_URL))