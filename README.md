# FastAPI + SQLite (zakladni vyukovy priklad)

Tento mini-projekt ukazuje uplny zaklad:
- `POST /mereni` ulozi data do SQLite tabulky
- `GET /prehled` zobrazi HTML tabulku s ulozenymi daty
- `GET /api/mereni` vrati stejna data jako JSON

Cil je ukázat:
- jak FastAPI prijima JSON data,
- jak se ukladaji data do SQLite,
- jak vratit jednoduchou HTML stranku s daty z DB.

## 1) Instalace
Vytvoříme virtuální python prostředí (.venv) umístěné ve složce projektu.
Prostředí aktivujeme a nainstalujeme knihovny.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 2) Spusteni aplikace

```bash
uvicorn app:app --reload
```

Aplikace pobezi na `http://127.0.0.1:8000`.

## 3) Vlozeni dat (POST /mereni)

Priklad JSONu:

```json
{
  "druh_mereni": "teplota",
  "hodnota": 23.7
}
```

Pole `tcas` je nepovinne. Kdyz ho neposles, ulozi se automaticky aktualni cas z DB.

Priklad s `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/mereni" ^
  -H "Content-Type: application/json" ^
  -d "{\"druh_mereni\":\"teplota\",\"hodnota\":23.7}"
```

## 4) Zobrazeni dat (GET /prehled)

Otevri v prohlizeci:

`http://127.0.0.1:8000/prehled`

Uvidis HTML tabulku s daty z SQLite.

## 5) JSON API (GET /api/mereni)

Otevri v prohlizeci nebo v API klientovi:

`http://127.0.0.1:8000/api/mereni`

Dostanes JSON pole zaznamu z tabulky.

Jednoduchy filtr podle typu mereni:

`http://127.0.0.1:8000/api/mereni?druh_mereni=teplota`

## 6) Struktura tabulky

Tabulka `mereni` ma sloupce:
- `tcas` (TEXT, defaultne se doplni automaticky)
- `druh_mereni` (TEXT)
- `hodnota` (REAL)

Interni sloupec `id` je primarni klic pro snadne razeni a identifikaci zaznamu.

## 7) Co zkusit dal

- pridej filtr podle typu mereni,
- pridej validaci povoleneho rozsahu `hodnota`,
- pridej endpoint pro mazani dat.
