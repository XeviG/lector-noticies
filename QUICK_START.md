# ⚡ Guia ràpida

## Opció 1 · Local

```bash
pip install -r requirements.txt
python update_news.py
open index.html
```

Executa `python update_news.py` cada dia per actualitzar les notícies.

## Opció 2 · Automàtic (recomanat)

1. Puja els fitxers a un repositori GitHub **públic**.
2. El workflow `.github/workflows/update.yml` s'executa sol cada matí (06:00 UTC = 08:00 a Catalunya a l'estiu).
3. Activa **GitHub Pages** → Settings → Pages → *Source: GitHub Actions*.
4. Obre la teva URL pública: `https://<usuari>.github.io/<repositori>/`.

## Què fa l'script

- Llegeix feeds RSS públics de les 5 categories (esports, tecnologia, macroeconomia, política catalana i educació).
- Política catalana i educació: **només fonts catalanes en català**.
- Genera `news.json` amb titular, resum, font, data i rellevància per a l'audiència.
- Filtra notícies de més de 48 hores i elimina duplicats.

## Comprovació ràpida

1. Executa `python update_news.py`.
2. Obre `index.html`.
3. Si veus notícies en 5 seccions, **funciona** ✅

## Errors habituals

| Error | Solució |
|---|---|
| `feedparser` no trobat | `pip install -r requirements.txt` |
| Notícies buides | Espera una altra execució o revisa els logs d'Actions |
| GitHub Actions no s'executa | Comprova que el repo és públic i que el fitxer està a `.github/workflows/` |