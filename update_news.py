#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Actualitzador de notícies des de feeds RSS internacionals
Genera un arxiu news.json amb les últimes notícies
"""

import feedparser
import json
from datetime import datetime
import time
import re

# Feeds RSS internacionals per categoria
FEEDS = {
    'sports': [
        {
            'url': 'https://feeds.espn.com/feeds/site/espneurope/nba',
            'source': 'ESPN NBA',
            'limit': 3
        },
        {
            'url': 'https://www.rugbyrama.fr/rss/flux/toute-l-actualite',
            'source': 'Rugbyrama',
            'limit': 2
        },
        {
            'url': 'https://www.worldathletics.org/rss/news',
            'source': 'World Athletics',
            'limit': 2
        }
    ],
    'tech': [
        {
            'url': 'https://feeds.arstechnica.com/arstechnica/index',
            'source': 'Ars Technica',
            'limit': 3
        },
        {
            'url': 'https://www.theverge.com/rss/index.xml',
            'source': 'The Verge',
            'limit': 2
        },
        {
            'url': 'https://hnrss.org/frontpage',
            'source': 'Hacker News',
            'limit': 2
        }
    ],
    'economy': [
        {
            'url': 'https://feeds.reuters.com/finance/markets',
            'source': 'Reuters Finance',
            'limit': 3
        },
        {
            'url': 'https://feeds.bloomberg.com/markets/news.rss',
            'source': 'Bloomberg Markets',
            'limit': 2
        },
        {
            'url': 'https://feeds.cnbc.com/id/100003114/device/rss/rss.html',
            'source': 'CNBC',
            'limit': 2
        }
    ],
    'politics': [
        {
            'url': 'https://feeds.bbc.co.uk/news/world/europe/rss.xml',
            'source': 'BBC Europe',
            'limit': 2
        },
        {
            'url': 'https://feeds.reuters.com/reuters/worldNews',
            'source': 'Reuters World',
            'limit': 2
        },
        {
            'url': 'https://www.france24.com/en/europe/rss',
            'source': 'France 24 Europe',
            'limit': 2
        },
        {
            'url': 'https://www.ara.cat/rss/politica/',
            'source': 'ARA Política',
            'limit': 2
        },
        {
            'url': 'https://www.vilaweb.cat/feed/',
            'source': 'VilaWeb',
            'limit': 2
        }
    ],
    'education': [
        {
            'url': 'https://feeds.bbc.co.uk/news/rss.xml',
            'source': 'BBC News',
            'limit': 2
        },
        {
            'url': 'https://feeds.theguardian.com/theguardian/education/rss',
            'source': 'The Guardian Education',
            'limit': 2
        },
        {
            'url': 'https://feeds.reuters.com/reuters/lifeNews',
            'source': 'Reuters Life',
            'limit': 1
        }
    ]
}

CATEGORY_LABELS = {
    'sports': 'Esports',
    'tech': 'Tecnologia',
    'economy': 'Macroeconomia',
    'politics': 'Política',
    'education': 'Educació'
}

SUBCATEGORY_LABELS = {
    'sports': ['Esports', 'NBA', 'Rugby', 'Atletisme'],
    'tech': ['Tecnologia', 'IA', 'Ciberseguretat', 'Innovació'],
    'economy': ['Macroeconomia', 'Mercats', 'Economia Global', 'Finances'],
    'politics': ['Política', 'Europa', 'Notícies Internacionals'],
    'education': ['Educació', 'Universitats', 'Formació']
}

def clean_text(text):
    """Elimina etiquetes HTML i neteja el text"""
    if not text:
        return ""
    
    # Elimina etiquetes HTML
    text = re.sub(r'<[^>]+>', '', text)
    # Elimina múltiples espais
    text = re.sub(r'\s+', ' ', text)
    # Elimina salts de línia
    text = text.replace('\n', ' ').replace('\r', '')
    return text.strip()

def get_relative_time(pub_date):
    """Converteix una data a format relatiu (fa X hores)"""
    if not pub_date:
        return "Recent"
    
    try:
        # feedparser retorna time_struct
        import calendar
        pub_timestamp = calendar.timegm(pub_date)
        now_timestamp = time.time()
        diff = now_timestamp - pub_timestamp
        
        if diff < 3600:
            minutes = int(diff / 60)
            return f"fa {minutes} min" if minutes > 1 else "fa poc"
        elif diff < 86400:
            hours = int(diff / 3600)
            return f"fa {hours}h" if hours > 1 else "fa 1h"
        elif diff < 604800:
            days = int(diff / 86400)
            return f"fa {days}d" if days > 1 else "fa 1d"
        else:
            return "fa més d'una setmana"
    except:
        return "Recent"

def fetch_feed(feed_url, source_name, limit):
    """Obté notícies d'un feed RSS"""
    news_items = []
    
    try:
        feed = feedparser.parse(feed_url)
        entries = feed.entries[:limit]
        
        for entry in entries:
            try:
                title = clean_text(entry.get('title', 'Sense títol'))
                summary = clean_text(entry.get('summary', entry.get('description', '')))
                
                # Talla el resum a 150 caràcters
                if len(summary) > 150:
                    summary = summary[:150] + '…'
                
                pub_date = entry.get('published_parsed', None)
                relative_time = get_relative_time(pub_date)
                
                if title and summary:  # Solo inclou si té títol i resum
                    news_items.append({
                        'title': title,
                        'summary': summary,
                        'source': source_name,
                        'date': relative_time,
                        'link': entry.get('link', '#')
                    })
            except Exception as e:
                print(f"⚠️  Error processant entrada de {source_name}: {e}")
                continue
        
        print(f"✅ {source_name}: {len(news_items)} notícies")
        
    except Exception as e:
        print(f"❌ Error llegint {source_name}: {e}")
    
    return news_items

def get_category_label(category, news_title):
    """Assigna una subcategoria segons el títol"""
    title_lower = news_title.lower()
    subcategories = SUBCATEGORY_LABELS.get(category, [])
    
    for subcat in subcategories[1:]:  # Saltem el primer que és genèric
        if subcat.lower() in title_lower:
            return f"{CATEGORY_LABELS.get(category, category)} - {subcat}"
    
    return CATEGORY_LABELS.get(category, category)

def update_news():
    """Actualitza totes les notícies"""
    print("\n🚀 Iniciant actualització de notícies...")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    all_news = []
    
    for category, feed_list in FEEDS.items():
        print(f"\n📺 Categoria: {CATEGORY_LABELS[category]}")
        print("-" * 40)
        
        for feed_config in feed_list:
            news_items = fetch_feed(
                feed_config['url'],
                feed_config['source'],
                feed_config['limit']
            )
            
            # Afegeix la categoria a cada notícia
            for item in news_items:
                item['category'] = category
                item['categoryLabel'] = get_category_label(category, item['title'])
                all_news.append(item)
            
            time.sleep(1)  # Pausa entre requests
    
    # Ordena per data (més recent primer) i limita a 50 notícies
    all_news = all_news[:50]
    
    # Crea l'estructura JSON
    data = {
        'lastUpdate': datetime.now().isoformat(),
        'totalNews': len(all_news),
        'news': all_news
    }
    
    # Guarda en JSON
    try:
        with open('news.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✨ {len(all_news)} notícies guardades en news.json")
        print(f"⏱️  Última actualització: {data['lastUpdate']}")
        print("\n✅ OPERACIÓ COMPLETADA!\n")
        
    except Exception as e:
        print(f"\n❌ Error guardant JSON: {e}\n")

if __name__ == '__main__':
    update_news()
