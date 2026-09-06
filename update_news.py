#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import calendar
import json
import os
import re
import time
from datetime import datetime, timezone
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

import feedparser

try:
    from langdetect import detect as detect_language, DetectorFactory

    DetectorFactory.seed = 0
except ImportError:
    detect_language = None

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
MAX_AGE_HOURS = 48
MAX_TOTAL_NEWS = 45
CATALONIA_TZ = ZoneInfo("Europe/Madrid")

TRANSLATE_TARGET = "ca"
TRANSLATE_ENDPOINT = os.environ.get("TRANSLATE_ENDPOINT", "").strip()
TRANSLATION_EMAIL = os.environ.get("TRANSLATION_EMAIL", "").strip()

CATALAN_SOURCES = {"ARA", "VilaWeb", "NacióDigital", "El Diari de l'Educació"}

SOURCE_LANGS = {
    "Rugbyrama": "fr",
    "Investing.com": "es",
    "Yahoo Finance": "en",
    "Yahoo Sports NBA": "en",
    "Ars Technica": "en",
    "The Verge": "en",
    "The Hacker News": "en",
    "BleepingComputer": "en",
    "TechCrunch": "en",
    "Wired": "en",
    "CNBC": "en",
    "MarketWatch": "en",
    "Bloomberg Markets": "en",
}

CATEGORY_LABELS = {
    "sports": "Esports",
    "tech": "Tecnologia",
    "economy": "Macroeconomia",
    "politics": "Política Catalana",
    "education": "Educació",
}

CATEGORY_ORDER = ["sports", "tech", "economy", "politics", "education"]

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


def _fetch_text(url):
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    with urlopen(req, timeout=25) as resp:
        return resp.read().decode("utf-8")


def webapp_translate(text):
    if not TRANSLATE_ENDPOINT:
        return None
    url = (
        f"{TRANSLATE_ENDPOINT}?"
        f"{urlencode({'q': text, 'tl': TRANSLATE_TARGET})}"
    )
    for attempt in range(2):
        try:
            out = _fetch_text(url)
            return out.strip() or None
        except (HTTPError, OSError):
            if attempt == 0:
                time.sleep(2)
    return None


def google_translate(text, source_lang):
    params = {
        "client": "gtx",
        "sl": source_lang or "auto",
        "tl": TRANSLATE_TARGET,
        "dt": "t",
        "q": text,
    }
    url = (
        "https://translate.googleapis.com/translate_a/single?"
        f"{urlencode(params)}"
    )
    try:
        data = json.loads(_fetch_text(url))
        return "".join(seg[0] for seg in data[0] if seg and seg[0]) or None
    except (HTTPError, OSError):
        return None


def mymemory_translate(text, source_lang):
    if not source_lang:
        return None
    params = {"q": text, "langpair": f"{source_lang}|{TRANSLATE_TARGET}"}
    if TRANSLATION_EMAIL:
        params["de"] = TRANSLATION_EMAIL
    url = f"https://api.mymemory.translated.net/get?{urlencode(params)}"
    for attempt in range(2):
        try:
            data = json.loads(_fetch_text(url))
            if data.get("responseStatus") == 200:
                out = data.get("responseData", {}).get("translatedText")
                return out or None
        except (HTTPError, OSError):
            if attempt == 0:
                time.sleep(2)
    return None


def translate_text(text, source_lang):
    if not text:
        return text
    if detect_language is not None:
        try:
            if detect_language(text) == "ca":
                return text
        except Exception:
            pass
    lang = source_lang
    if lang is None and detect_language is not None:
        try:
            lang = detect_language(text)
        except Exception:
            lang = None
    out = webapp_translate(text)
    if not out:
        out = mymemory_translate(text, lang)
    if not out:
        out = google_translate(text, lang)
    return out or text


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
        title_out = title
        summary_out = summary
        if config["source"] not in CATALAN_SOURCES:
            title_out = translate_text(
                title, SOURCE_LANGS.get(config["source"])
            )
            if summary_out:
                summary_out = translate_text(
                    summary_out, SOURCE_LANGS.get(config["source"])
                )
            time.sleep(0.15)
        if len(summary_out) > 180:
            summary_out = summary_out[:180].rsplit(" ", 1)[0] + "…"
        pub = published_info(entry.get("published_parsed"))
        items.append(
            {
                "title": title_out,
                "summary": summary_out,
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