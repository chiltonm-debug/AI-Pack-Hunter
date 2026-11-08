#!/usr/bin/env python3
"""Build conservative, unverified TCG promotion leads from Google News RSS.
Only retain RSS results whose publisher metadata matches an allowlisted official domain.
No target-site crawling, login, claims, or purchases are performed.
"""
import json, re, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

QUERIES = [
    ("Pokémon", 'site:play.pokemon.com OR site:pokemon.com OR site:community.pokemon.com Pokémon TCG (free OR giveaway OR prize OR reward OR promotional pack OR code card)'),
    ("One Piece", 'site:en.onepiece-cardgame.com OR site:one-piece.com/news One Piece Card Game (free OR giveaway OR prize OR reward OR campaign OR present)'),
]
ALLOWED = {
    "play.pokemon.com", "pokemon.com", "community.pokemon.com",
    "en.onepiece-cardgame.com", "one-piece.com", "shop.bandainamco-am.com",
}
TERMS = re.compile(r"free|giveaway|give away|prize|reward|promotional|promo|code card|campaign|present|プレゼント|キャンペーン|配布|無料", re.I)
TCG = re.compile(r"pokemon|pokémon|ポケモンカード|one piece|ワンピースカード|card game|tcg", re.I)
EXCLUDE = re.compile(r"pre.?order|release date|available now|buy now|price|new product", re.I)
UA = "AI-Pack-Hunter-Opportunity-Discovery/1.0 (+https://github.com/chiltonm-debug/AI-Pack-Hunter)"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rss+xml, application/xml, text/xml"})
    with urllib.request.urlopen(req, timeout=25) as response:
        return response.read(), response.geturl()

def is_official_source(source_url):
    host = (urllib.parse.urlparse(source_url).hostname or "").lower()
    return any(host == d or host.endswith("." + d) for d in ALLOWED)

def main():
    found = {}
    for game, query in QUERIES:
        params = urllib.parse.urlencode({"q": query, "hl": "en-US", "gl": "US", "ceid": "US:en"})
        feed_url = "https://news.google.com/rss/search?" + params
        try:
            raw, _ = fetch(feed_url)
            root = ET.fromstring(raw)
            for item in root.findall(".//item")[:30]:
                title = (item.findtext("title") or "").strip()
                description = re.sub(r"<[^>]+>", " ", item.findtext("description") or "").strip()
                link = (item.findtext("link") or "").strip()
                pub = (item.findtext("pubDate") or "").strip()
                source_el = item.find("source")
                source_name = source_el.text.strip() if source_el is not None and source_el.text else "News result"
                text = title + " " + description
                if not title or not link or not TERMS.search(text) or not TCG.search(text) or EXCLUDE.search(title):
                    continue
                source_url = source_el.attrib.get("url", "") if source_el is not None else ""
                if not is_official_source(source_url):
                    continue
                # Keep the RSS redirect link; do not fetch or crawl the publisher page.
                key = link
                found[key] = {
                    "id": key, "game": game, "title": title, "url": link,
                    "source": source_name, "sourceUrl": source_url, "published": pub,
                    "summary": description[:360],
                    "status": "Needs manual verification",
                    "cost": "Unknown", "confirmedFree": False,
                    "note": "Candidate only. Check the official terms, eligibility, total cost, deposit/subscription requirements, region, and expiry before treating this as free."
                }
            time.sleep(2)
        except Exception as exc:
            print(f"Feed query failed for {game}: {exc}")
    output = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "method": "Google News RSS discovery; publisher metadata must match allowlisted official domains; publisher pages are not crawled",
        "items": sorted(found.values(), key=lambda x: x.get("published", ""), reverse=True)[:40],
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/discoveries.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(output['items'])} unverified official-domain candidate leads.")

if __name__ == "__main__":
    main()
