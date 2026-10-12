from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
import json
import re
import xml.etree.ElementTree as ET

FEED_URL = "https://medium.com/feed/@0xasmaa"
OUTPUT = Path("_data/medium_posts.json")
MAX_POSTS = 10


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def plain_text(value):
    parser = TextExtractor()
    parser.feed(value or "")
    return re.sub(r"\s+", " ", " ".join(parser.parts)).strip()


def main():
    request = Request(
        FEED_URL,
        headers={"User-Agent": "Mozilla/5.0 (compatible; AsmaaPortfolioFeed/1.0)"},
    )
    with urlopen(request, timeout=30) as response:
        xml_data = response.read()

    feed = ET.fromstring(xml_data)
    posts = []

    for item in feed.findall("./channel/item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        # Only publish links from Medium's own domain.
        if not title or not link.startswith("https://medium.com/"):
            continue

        description = plain_text(item.findtext("description") or "")
        if len(description) > 220:
            description = description[:217].rsplit(" ", 1)[0] + "..."

        raw_date = item.findtext("pubDate") or ""
        try:
            published = parsedate_to_datetime(raw_date).date().isoformat()
        except (TypeError, ValueError, OverflowError):
            published = ""

        posts.append({
            "title": title,
            "link": link,
            "description": description,
            "published": published,
        })
        if len(posts) >= MAX_POSTS:
            break

    if not posts:
        raise RuntimeError("No Medium articles were found in the RSS feed; existing data was not overwritten.")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(posts, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Saved {len(posts)} Medium articles to {OUTPUT}")


if __name__ == "__main__":
    main()
