# 📰 Lector de Notícies del Dia · Agregador en Català

Agregador intel·ligent de notícies diàries **en català** que recopila contingut de les 5 àrees següents i es publica automàticament cada matí, **sense cap cost**.

- 🏀 **Esports**: NBA, Rugby Top 14, Atletisme (Diamond League)
- 💻 **Tecnologia**: IA, ciberseguretat, startups i inversions, productes, tendències digitals
- 💰 **Macroeconomia**: borsa i mercats (**IBEX-35**, **CAC-40**), inflació, tipus d'interès
- 🏛️ **Política Catalana** (només fonts catalanes en català)
- 📚 **Educació** (només fonts catalanes en català)

---

## 🚀 Funcionament

1. **`update_news.py`** llegeix feeds RSS públics i verificats de cada categoria.
2. Genera **`news.json`** amb titular, resum, font, data de publicació i **context de rellevància** per a l'audiència catalana.
3. **`index.html`** mostra les notícies organitzades per categories, amb les més recents al principi de cada secció.
4. **GitHub Actions** executa el guió cada matí i **GitHub Pages** publica el resultat en una URL fixa.

---

## ⚡ Ús local

```bash
pip install -r requirements.txt
python update_news.py
```

Obre `index.html` al navegador. Torna a executar el guió cada dia per actualitzar.

---

## 🤖 Automatització diària

El workflow `.github/workflows/update.yml` s'executa cada matí a les **06:00 UTC** (08:00 hora de Catalunya a l'estiu). Amb el workflow `.github/workflows/pages.yml`, tots els canvis a `main` es publiquen automàticament a GitHub Pages.

**Per activar GitHub Pages al teu repositori:**
1. Vés a **Settings → Pages**.
2. A **Build and deployment**, escull *Source* → **GitHub Actions**.
3. La URL pública serà `https://<usuari>.github.io/<repositori>/`.

---

## 📰 Fonts de notícies

### Esports
| Subcategoria | Fonts |
|---|---|
| NBA | Yahoo Sports NBA |
| Rugby Top 14 | Rugbyrama |
| Atletisme | World Athletics, Diamond League |

### Tecnologia
| Subcategoria | Fonts |
|---|---|
| IA i machine learning | The Verge AI |
| Ciberseguretat | The Hacker News, BleepingComputer |
| Startups i inversions | TechCrunch |
| Productes i llançaments | The Verge, Ars Technica |
| Tendències digitals | Wired |

### Macroeconomia
| Subcategoria | Fonts |
|---|---|
| IBEX-35 | Yahoo Finance |
| CAC-40 | Yahoo Finance |
| Mercats i borsa | CNBC, MarketWatch, Bloomberg Markets |
| Mercats europeus | Investing.com |

### Política Catalana (només català)
| Fonts |
|---|
| ARA · VilaWeb · NacióDigital |

### Educació (només català)
| Subcategoria | Fonts |
|---|---|
| Sistema educatiu | El Diari de l'Educació |
| Polítiques educatives | ARA (societat) |

---

## 📋 Format de sortida

Cada notícia de `news.json` conté:

```json
{
  "title": "Titular",
  "summary": "Resum en 2-3 frases",
  "published": "2026-09-06T06:00:00+00:00",
  "date": "fa 2 h",
  "source": "Font",
  "link": "https://…",
  "category": "sports",
  "categoryLabel": "Esports · NBA",
  "subcategory": "NBA",
  "connection": "Per què és rellevant per a l'audiència"
}
```

Criteris de qualitat aplicats: només fonts reconegudes, prioritat a les **últimes 24-48 hores**, **deduplicació** per títol i enllaç, i ordenació per recència dins de cada secció.

---

## 🛠️ Personalització

### Afegir o canviar fonts

Edita el diccionari `FEEDS` a `update_news.py`:

```python
'categoria': [
    {
        'url': 'https://exemple.com/rss',
        'source': 'Nom de la font',
        'subcategory': 'Subcategoria',
        'limit': 2,
    },
]
```

### Limitar el total de notícies

Canvia `MAX_TOTAL_NEWS` (per defecte 45) a `update_news.py`.

### Canviar la finestra temporal

Canvia `MAX_AGE_HOURS` (per defecte 48 hores). Si una secció queda buida, s'inclou el contingut més recent disponible perquè no quedi mai sense notícies.

### Canviar l'hora d'actualització

A `.github/workflows/update.yml`, la línia:

```yaml
- cron: '0 6 * * *'
```

---

## 🔍 Solucionar problemes

| Problema | Solució |
|---|---|
| `ModuleNotFoundError: feedparser` | `pip install -r requirements.txt` |
| `news.json` no existeix | Executa `python update_news.py` |
| Notícies desactualitzades | Vés a la pestanya **Actions** de GitHub i consulta el log |
| La web no es veu | Comprova que **GitHub Pages** està activada (Settings → Pages → GitHub Actions) |

---

## 💰 Cost

**0 €.** Python és lliure, els feeds RSS són públics, GitHub Actions permet 2.000 minuts al mes i GitHub Pages és gratuït.