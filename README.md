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
2. **Tradueix automàticament al català** el títol i el resum de cada notícia (els enllaços continuen apuntant a l'idioma original de la font).
3. Genera **`news.json`** amb titular, resum, font i data de publicació.
4. **`index.html`** mostra les notícies organitzades per categories, amb les més recents al principi de cada secció, i tot el text en català.
5. **GitHub Actions** executa el guió cada matí i **GitHub Pages** publica el resultat en una URL fixa.

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
  "title": "Titular (en català)",
  "summary": "Resum (traduït al català)",
  "published": "2026-09-06T06:00:00+00:00",
  "date": "fa 2 h",
  "source": "Font",
  "link": "https://…",
  "category": "sports",
  "categoryLabel": "Esports · NBA",
  "subcategory": "NBA"
}
```

Criteris de qualitat aplicats: només fonts reconegudes, prioritat a les **últimes 24-48 hores**, **deduplicació** per títol i enllaç, i ordenació per recència dins de cada secció.

---

## 🌐 Traducció automàtica al català

El lector mostra **tot** (títols i resums) en català, gràcies a un traductor gratuït de Google. Quan fas clic a una notícia, obres l'article original en l'idioma de la font.

### 1. Crea l'Apps Script (2 minuts)

1. Vés a [script.google.com](https://script.google.com) i prem **Nou projecte**.
2. Esborra el contingut de l'editor i enganxa el fitxer **`appsscript.gs`** d'aquest repositori.
3. Prem **Desplega → Nou desplegament → Aplicació web**.
4. A **Executar com a** → *Jo (el teu compte)* i a **Qui pot accedir** → *Qualsevol*.
5. Prem **Desplegar**, accepta els permisos i **copia la URL** (acaba en `/exec`).

### 2. Desa la URL en un secret de GitHub

1. Al repositori: **Settings → Secrets and variables → Actions → New repository secret**.
2. **Name:** `TRANSLATE_ENDPOINT`
3. **Secret:** la URL copiada.

A partir del proper dia, tot es rebrà traduït. Mentre el secret no existeix, el guió prova altres traductors públics gratuïts i, si cap no respon, deixa el text original (mai no es trenca).

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