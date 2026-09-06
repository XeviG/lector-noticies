#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import calendar
import json
import re
import time
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import feedparser

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
MAX_AGE_HOURS = 48
MAX_TOTAL_NEWS = 45
CATALONIA_TZ = ZoneInfo("Europe/Madrid")

CATEGORY_LABELS = {
    "sports": "Esports",
    "tech": "Tecnologia",
    "economy": "Macroeconomia",
    "politics": "Política Catalana",
    "education": "Educació",
}

CATEGORY_ORDER = ["sports", "tech", "economy", "politics", "education"]

CONNECTIONS = {
    "sports": "Rellevant per a l'audiència esportiva catalana, que segueix de prop les competicions internacionals com la NBA, el Top 14 o la Diamond League.",
    "tech": "D'interès directe per al sector tecnològic i digital català, un dels ecosistemes més actius del sud d'Europa.",
    "economy": "Els mercats europeus i els tipus d'interès condicionen directament l'economia catalana, molt vinculada a l'exportació i a la inversió estrangera.",
    "politics": "Tracta decisions i acords que afecten directament les institucions i la ciutadania de Catalunya.",
    "education": "Afecta el sistema educatiu i la comunitat docent i universitària de Catalunya i de tot l'àmbit de parla catalana.",
}

FEEDS = {
    "sports": [
        {
            "url": "https://sports.yahoo.com/nba/rss/",
            "source": "Yahoo Sports NBA",
            "subcategory": "NBA",
            "limit": 3,
        },
        {
            "url": "https://www.rugbyrama.fr/rugby/top-14/rss.xml",
            "source": "Rugbyrama",
            "subcategory": "Rugby Top 14",
            "limit": 3,
        },
        {
            "url": "https://worldathletics.org/rss",
            "source": "World Athletics",
            "subcategory": "Atletisme",
            "limit": 2,
        },
        {
            "url": "https://www.diamondleague.com/rss",
            "source": "Diamond League",
            "subcategory": "Atletisme",
            "limit": 2,
        },
    ],
    "tech": [
        {
            "url": "https://feeds.arstechnica.com/arstechnica/index",
            "source": "Ars Technica",
            "subcategory": "Tecnologia",
            "limit": 1,
        },
        {
            "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
            "source": "The Verge",
            "subcategory": "IA i machine learning",
            "limit": 2,
        },
        {
            "url": "https://feeds.feedburner.com/TheHackersNews",
            "source": "The Hacker News",
            "subcategory": "Ciberseguretat",
            "limit": 2,
        },
        {
            "url": "https://www.bleepingcomputer.com/feed/",
            "source": "BleepingComputer",
            "subcategory": "Ciberseguretat",
            "limit": 2,
        },
        {
            "url": "https://techcrunch.com/feed/",
            "source": "TechCrunch",
            "subcategory": "Startups i inversions",
            "limit": 2,
        },
        {
            "url": "https://www.theverge.com/rss/index.xml",
            "source": "The Verge",
            "subcategory": "Productes i llançaments",
            "limit": 1,
        },
        {
            "url": "https://www.wired.com/feed/rss",
            "source": "Wired",
            "subcategory": "Tendències digitals",
            "limit": 1,
        },
    ],
    "economy": [
        {
            "url": "https://finance.yahoo.com/rss/index?s=%5EIBEX",
            "source": "Yahoo Finance",
            "subcategory": "IBEX-35",
            "limit": 2,
        },
        {
            "url": "https://finance.yahoo.com/rss/index?s=%5EFCHI",
            "source": "Yahoo Finance",
            "subcategory": "CAC-40",
            "limit": 2,
            "fallback_urls": [
                "https://finance.yahoo.com/rss/headline?s=%5EFCHI"
            ],
        },
        {
            "url": "https://www.investing.com/rss/news_1.rss",
            "source": "Investing.com",
            "subcategory": "Mercats europeus",
            "limit": 2,
        },
        {
            "url": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258",
            "source": "CNBC",
            "subcategory": "Mercats i borsa",
            "limit": 2,
        },
        {
            "url": "https://feeds.marketwatch.com/marketwatch/topstories/",
            "source": "MarketWatch",
            "subcategory": "Mercats i borsa",
            "limit": 2,
        },
        {
            "url": "https://feeds.bloomberg.com/markets/news.rss",
            "source": "Bloomberg Markets",
            "subcategory": "Mercats i borsa",
            "limit": 2,
        },
    ],
    "politics": [
        {
            "url": "https://www.ara.cat/rss/politica/",
            "source": "ARA",
            "subcategory": "Generalitat i Parlament",
            "limit": 4,
        },
        {
            "url": "https://www.vilaweb.cat/feed/",
            "source": "VilaWeb",
            "subcategory": "Actualitat catalana",
            "limit": 4,
        },
        {
            "url": "https://www.naciodigital.cat/rss",
            "source": "NacióDigital",
            "subcategory": "Actualitat catalana",
            "limit": 3,
        },
    ],
    "education": [
        {
            "url": "https://diarieducacio.cat/feed/",
            "source": "El Diari de l'Educació",
            "subcategory": "Sistema educatiu",
            "limit": 6,
        },
        {
            "url": "https://www.ara.cat/rss/societat/",
            "source": "ARA",
            "subcategory": "Polítiques educatives",
            "limit": 3,
        },
    ],
}


def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text)
    text = text.replace("\n", " ").replace("\r", "")
    return text.strip()


def relative_time(published_parsed):
    if not published_parsed:
        return "Recent"
    try:
        published_stamp = calendar.timegm(published_parsed)
        now_stamp = time.time()
        diff = now_stamp - published_stamp
        if diff < 3600:
            minutes = int(diff / 60)
            return f"fa {minutes} min" if minutes > 1 else "fa poc"
        if diff < 86400:
            hours = int(diff / 3600)
            return f"fa {hours} h" if hours > 1 else "fa 1 h"
        if diff < 604800:
            days = int(diff / 86400)
            return f"fa {days} d" if days > 1 else "fa 1 d"
        return "fa més d'una setmana"
    except Exception:
        return "Recent"


def published_info(published_parsed):
    if not published_parsed:
        return {"published": None, "publishedLocal": None}
    try:
        published_stamp = calendar.timegm(published_parsed)
        dt_utc = datetime.fromtimestamp(published_stamp, timezone.utc)
        dt_cat = dt_utc.astimezone(CATALONIA_TZ)
        return {
            "published": dt_utc.isoformat(timespec="seconds"),
            "publishedLocal": dt_cat.strftime("%d/%m/%Y %H:%M"),
        }
    except Exception:
        return {"published": None, "publishedLocal": None}


def is_recent(published_parsed):
    if not published_parsed:
        return False
    try:
        published_stamp = calendar.timegm(published_parsed)
        return (time.time() - published_stamp) <= MAX_AGE_HOURS * 3600
    except Exception:
        return False


def normalize_title(title):
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def fetch_feed(config):
    items = []
    urls = [config["url"]] + config.get("fallback_urls", [])
    entries = []
    for url in urls:
        for attempt in range(4):
            try:
                parsed = feedparser.parse(
                    url,
                    request_headers={"User-Agent": USER_AGENT},
                )
                entries = parsed.entries
                if entries:
                    break
            except Exception as exc:
                print(f"[-] {config['source']} (intent {attempt + 1}): {exc}")
                entries = []
            if attempt < 3:
                time.sleep(2 * (attempt + 1))
        if entries:
            break

    entries = entries[: config["limit"]]
    recent = [e for e in entries if is_recent(e.get("published_parsed"))]
    if not recent and entries:
        recent = entries
    for entry in recent[: config["limit"]]:
        title = clean_text(entry.get("title", ""))
        summary = clean_text(
            entry.get("summary", entry.get("description", ""))
        )
        if not title:
            continue
        if len(summary) > 160:
            summary = summary[:160].rsplit(" ", 1)[0] + "…"
        pub = published_info(entry.get("published_parsed"))
        items.append(
            {
                "title": title,
                "summary": summary,
                "published": pub["published"],
                "publishedLocal": pub["publishedLocal"],
                "date": relative_time(entry.get("published_parsed")),
                "source": config["source"],
                "link": entry.get("link", "#"),
                "category": config["category"],
                "categoryLabel": (
                    f"{CATEGORY_LABELS[config['category']]} · "
                    f"{config['subcategory']}"
                ),
                "subcategory": config["subcategory"],
                "connection": CONNECTIONS[config["category"]],
            }
        )
    return items


def main():
    print("Iniciant actualització de notícies...")
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    all_news = []
    seen_titles = set()
    seen_links = set()
    feed_stats = []

    for category in CATEGORY_ORDER:
        for config in FEEDS[category]:
            config = dict(config, category=category)
            items = fetch_feed(config)
            unique = []
            for item in items:
                key_title = normalize_title(item["title"])
                key_link = item["link"].split("?")[0].rstrip("/")
                if key_title in seen_titles or key_link in seen_links:
                    continue
                seen_titles.add(key_title)
                seen_links.add(key_link)
                unique.append(item)
            all_news.extend(unique)
            feed_stats.append(
                f"{config['source']}: {len(unique)} notícies"
            )
            time.sleep(1)

    all_news.sort(
        key=lambda n: n["published"] or "1970-01-01T00:00:00+00:00",
        reverse=True,
    )
    all_news = all_news[:MAX_TOTAL_NEWS]

    for stat in feed_stats:
        print(f"[+] {stat}")

    data = {
        "lastUpdate": datetime.now().astimezone(CATALONIA_TZ).isoformat(timespec="seconds"),
        "lastUpdateLocal": datetime.now().astimezone(CATALONIA_TZ).strftime("%d/%m/%Y %H:%M"),
        "totalNews": len(all_news),
        "categories": CATEGORY_LABELS,
        "news": all_news,
    }

    try:
        with open("news.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[OK] {len(all_news)} notícies guardades a news.json")
        print(f"[OK] Última actualització: {data['lastUpdate']}")
    except Exception as exc:
        print(f"[-] Error guardant news.json: {exc}")


if __name__ == "__main__":
    main()