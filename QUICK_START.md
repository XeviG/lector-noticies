# ⚡ INICI RÀPID (10 minuts)

Tria una opció i segueix els passos:

---

## ✅ OPCIÓ 1: Local (Tu ordinador)

### Pas 1: Instalar Python
- Baixa de: https://www.python.org/downloads/
- Selecciona la versió per a tu sistema operatiu
- Instal·la amb les opcions per defecte

### Pas 2: Obrir terminal/consola
- **Windows**: Búsca "Símbol del sistema" o "PowerShell"
- **Mac**: Aplicacions > Utilitats > Terminal
- **Linux**: Obre la terminal

### Pas 3: Instal·lar dependències
Copia i enganxa aquesta comanda:

```
pip install feedparser
```

### Pas 4: Generar notícies
Copia i enganxa aquesta comanda:

```
python update_news.py
```

### Pas 5: Obrir el lector
1. Localitza l'arxiu `index.html` en la carpeta
2. Fes doble clic per obrir-lo en el navegador
3. **Llest!** 🎉

### Per actualitzar cada dia:
- Executa `python update_news.py` manualment
- O programar una tasca cada matí amb:
  - **Windows**: Planificador de tasques
  - **Mac**: launchd
  - **Linux**: crontab

---

## ⭐ OPCIÓ 2: GitHub Actions (AUTOMÀTIC)

### Pas 1: Crea una carpeta
Copia tots els arxius d'aquí en una carpeta nova.

### Pas 2: Crea un compte GitHub
- Vés a: https://github.com/signup
- Completa el formulari (gratis)
- Verifica el correu

### Pas 3: Crea un repositori
1. Vés a: https://github.com/new
2. **Nom**: `lector-notícies`
3. **Descripció**: "Agregador de notícies diaries"
4. **Marca PUBLIC** ⚠️ Important
5. Click "Create repository"

### Pas 4: Puja els arxius (opció web - més fàcil)

1. Dins del repositori, click "uploading an existing file"
2. Puja aquests arxius:
   - `update_news.py`
   - `index.html`
   - `requirements.txt`

3. Crea la carpeta `.github/workflows`:
   - Click "Create new file"
   - Nom: `.github/workflows/update.yml`
   - Copia el contingut de `github_workflow.yml`
   - Click "Commit new file"

### Pas 5: Activa GitHub Actions
1. Vés a la pestanya "Actions"
2. Si necessita permís, click al botó gris
3. Click "I understand my workflows, go ahead and enable them"

### Pas 6: Accedeix al lector

**Opció A - Veure arxiu raw:**
```
https://raw.githubusercontent.com/TU_USERNAME/lector-notícies/main/index.html
```
(Substituir TU_USERNAME per tu usuari de GitHub)

**Opció B - Publicar amb GitHub Pages (millor):**
1. Settings → Pages
2. Source: Branch main, folder /
3. Espera 1-2 minuts
4. URL: `https://TU_USERNAME.github.io/lector-notícies/`

### Resultat: ✅
- Cada dia a les 8:00 AM UTC (9:00 AM Catalunya), les notícies s'actualitzen automàticament
- No cal fer res més
- El lector sempre tindrà les últimes notícies

---

## 📊 Comparativa

| | Opció 1 | Opció 2 |
|---|---|---|
| Facilitat | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Setup | 5 min | 10 min |
| Actualització | Manual | Automàtica |
| Cost | Gratis | Gratis |
| Ideal per | Privat | Compartir |

---

## 🔍 Comprovar que funciona

### Opció 1:
1. Executa `python update_news.py`
2. Obrir `index.html`
3. Si veus 50 notícies, **funciona** ✅

### Opció 2:
1. Vés a "Actions" en GitHub
2. Veure si l'últim workflow té ✅
3. Accedeix a `index.html` en GitHub Pages
4. Si veus notícies, **funciona** ✅

---

## 🆘 Si algo falla

| Error | Solució |
|-------|---------|
| "Python not found" | Reinstal·la Python i reinicia |
| "ModuleNotFoundError: feedparser" | Executa: `pip install feedparser` |
| GitHub Actions no s'executa | Mira la pestanya "Actions" per errors |
| news.json buït | Executa `python update_news.py` manualment |
| Notícies buides | Recarga (Ctrl+Shift+R) o esborra cache |

---

## 🎯 Pròxim pas

1. **Prova la Opció 1** primer (més ràpid)
2. Si funciona, **migra a Opció 2** (més còmoda)
3. Personalitza les fonts si vols (mira `README.md`)

---

**Pregunta:** Tens Git instal·lat?
- **SÍ** → Usa `git clone` per descarregar tot
- **NO** → Descàrrega com ZIP des de GitHub i descomprimeix

```bash
# Si tens Git (més ràpid):
git clone https://github.com/TU_USER/lector-notícies.git
cd lector-notícies
python update_news.py
```

---

**Ara ja estàs llestos!** 🚀📰
