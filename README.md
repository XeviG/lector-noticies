# 📰 Lector de Notícies Diari - Guia Completa

Un agregador intel·ligent de notícies internacionals amb **actualització automàtica diària** sense cap cost.

---

## 🚀 INSTAL·LACIÓ RÀPIDA (5 minuts)

### **Opció A: Local (Ordinador)**

#### 1️⃣ **Instalar Python i dependències**

```bash
# Baixar Python desde https://www.python.org/downloads/
# O usar homebrew (Mac): brew install python3

# Instal·lar dependències
pip install feedparser
```

#### 2️⃣ **Executar el script**

```bash
python update_news.py
```

Això crearà un fitxer `news.json` amb les últimes notícies.

#### 3️⃣ **Obrir el lector**

1. Obrir `index.html` amb un navegador
2. Les notícies es carregaran automàticament

✅ **Ja funciona!** Pots executar `python update_news.py` cada matí manualment.

---

### **Opció B: Automatització amb GitHub (RECOMANAT) ⭐**

Això fa que s'actualitzi **sol cada matí** a les 8:00 AM.

#### 1️⃣ **Crea un repositori GitHub**

1. Vés a https://github.com/new
2. Nom: `lector-notícies` (o el que vulguis)
3. Marca "Public" (necessari perquè funcione)
4. Click "Create repository"

#### 2️⃣ **Puja els fitxers**

Pots fer-ho de dos maneres:

**Opció B1: Via web (més fàcil)**

1. Click "uploading an existing file"
2. Puja aquests fitxers:
   - `update_news.py`
   - `index.html`
   - `update.yml`

**Opció B2: Via terminal (més ràpid)**

```bash
# Clona el repositori
git clone https://github.com/TU_USER/lector-notícies.git
cd lector-notícies

# Copia els fitxers
mkdir -p .github/workflows
cp update_news.py .
cp index.html .
cp update.yml .github/workflows/

# Commit i push
git add .
git commit -m "Lector de notícies inicial"
git push
```

#### 3️⃣ **Configura GitHub Actions**

1. Vés al repositori
2. Click a la pestanya "Actions"
3. Click "set up a workflow yourself" (si no n'hi ha)
4. Copia el contingut de `update.yml` en l'editor
5. Commit (botó verde a dalt a la dreta)

#### 4️⃣ **Accedeix al lector**

1. Vés a: `https://raw.githubusercontent.com/TU_USER/lector-notícies/main/index.html`
2. O col·loca-ho en una carpeta web pública

✅ **Automàtic!** Cada matí a les 8:00 AM es descarregarà notícies noves.

---

## 📋 ESTRUCTURA DE FITXERS

```
lector-notícies/
├── update_news.py           # Script per baixar notícies
├── index.html               # Interfície del lector
├── news.json               # Notícies (generat automàticament)
├── .github/
│   └── workflows/
│       └── update.yml      # Configuració de GitHub Actions
└── README.md               # Aquesta guia
```

---

## 🎯 FUNCIONAMENT

### **Com funciona localment:**

```
1. Executar: python update_news.py
2. Script llegeix feeds RSS internacionals
3. Genera news.json amb 50 notícies máx
4. Obrir index.html al navegador
5. Les notícies es carreguen desde news.json
```

### **Com funciona amb GitHub:**

```
1. GitHub Actions executa update_news.py cada matí
2. Fa push de news.json actualitzat al repositori
3. index.html llegeix desde el repositori
4. Les notícies sempre estan actualitzades
```

---

## 📰 FONTS DE NOTÍCIES

El script llegeix de **fonts internacionals de qualitat**:

### **Esports**
- ESPN NBA
- Rugbyrama (Top 14)
- World Athletics (Diamond League)

### **Tecnologia**
- Ars Technica
- The Verge
- Hacker News

### **Macroeconomia**
- Reuters Finance
- Bloomberg Markets
- CNBC

### **Política**
- BBC Europe
- Reuters World
- France 24
- ARA (Català)
- VilaWeb (Català)

### **Educació**
- BBC News
- The Guardian Education
- Reuters Life

---

## 🔧 PERSONALITZACIÓ

### **Canviar hora d'actualització**

En `update.yml`, linea 10:

```yaml
- cron: '0 8 * * *'  # 8:00 AM UTC
```

Exemples:
- `'0 9 * * *'` → 9:00 AM
- `'30 7 * * *'` → 7:30 AM
- `'0 6 * * 1-5'` → 6:00 AM entre setmana

### **Afegir més fonts**

Edita `update_news.py` i afegeix nous feeds al diccionari `FEEDS`:

```python
'categoria': [
    {
        'url': 'https://example.com/rss',
        'source': 'Nom Font',
        'limit': 2
    }
]
```

### **Limitar notícies per categoria**

En `update_news.py`, busca `'limit': 3` i canvia el número.

---

## 🐛 SOLUCIONAR PROBLEMES

### **"No podem llegir news.json"**

Solució: Executa primer `python update_news.py` manualment.

### **GitHub Actions no s'executa**

Revisió:
1. El repositori és Public?
2. El fitxer `.github/workflows/update.yml` té el nom correcte?
3. Va a "Actions" i veure si hi ha errors

### **Les notícies no s'actualitzen**

1. Vés a GitHub "Actions"
2. Mira l'últim workflow
3. Si hi ha error, veure el log

---

## 📱 ÚS

### **Ordinador:**
- Obrir `index.html` en navegador
- Filtrar per categoria
- Mode clar/fosc

### **Mòbil:**
- Suscripció als favorits del navegador
- Totalment responsive
- Funciona sense instal·lació

---

## 💡 CONSELLS

1. **Primer cop**: Executa `python update_news.py` manualment per generar `news.json`

2. **GitHub Pages** (opcional): Pots publicar el `index.html` en GitHub Pages per tenir URL fixa:
   - Vés a Settings → Pages
   - Branch: main
   - Folder: / (root)
   - URL: `https://TU_USER.github.io/lector-notícies/`

3. **Backup local**: Sempre pots fer backup del `news.json` si tems perdre-ho

4. **Compartir**: Pots compartir la URL de `index.html` amb altres

---

## 🆓 COST

- **$0** - Tot és gratuït
- Python: Lliure i obert
- GitHub Actions: 2000 min/mes gratis
- RSS Feeds: Tots públics

---

## 📞 SUPORT RÀPID

| Problema | Solució |
|----------|---------|
| Python no instal·lat | Baixa de https://www.python.org |
| feedparser error | `pip install feedparser` |
| news.json no existeix | Executa `python update_news.py` |
| GitHub Actions error | Mira la pestanya "Actions" del repo |
| Notícies no apareixen | Recarga la pàgina (Ctrl+Shift+R) |

---

**Preguntes?** Pots revisar els logs de GitHub Actions o executar el script manualment per veure errors.

¡Que gaudeixis! 📰✨
