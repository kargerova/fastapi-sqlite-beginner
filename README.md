# FastAPI + SQLite (zakladni vyukovy priklad)

Tento mini-projekt ukazuje uplny zaklad:
- `POST /mereni_doma` ulozi data do SQLite tabulky
- `GET /mereni_doma_prehled` zobrazi HTML tabulku s ulozenymi daty
- `GET /mereni_doma` vrati stejna data jako JSON
- `GET /docs` zobrazi automaticky generovanou API dokumentaci

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

FastAPI automaticky poskytuje interaktivni dokumentaci na:

`http://127.0.0.1:8000/docs`

## 3) Vlozeni dat (POST /mereni_doma)

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
curl -X POST "http://127.0.0.1:8000/mereni_doma" ^
  -H "Content-Type: application/json" ^
  -d "{\"druh_mereni\":\"teplota\",\"hodnota\":23.7}"
```

## 4) Endpointy se sablonami (HTML)

Otevri v prohlizeci:

- `http://127.0.0.1:8000/mereni_doma_prehled`
- `http://127.0.0.1:8000/mereni_doma_prehled2`

Uvidis HTML tabulky s daty z SQLite.

Graf v case (parametrem je druh mereni):

- `http://127.0.0.1:8000/mereni_doma_graf?druh_mereni=teplota`
- `http://127.0.0.1:8000/mereni_doma_graf?druh_mereni=teplota%20podlaha`

Poznamka: mezera v URL se zapisuje jako `%20`.

## 5) JSON API (GET /mereni_doma)

Otevri v prohlizeci nebo v API klientovi:

`http://127.0.0.1:8000/mereni_doma`

Dostanes JSON pole zaznamu z tabulky.

Jednoduchy filtr podle typu mereni:

`http://127.0.0.1:8000/mereni_doma?druh_mereni=teplota`

## 6) Struktura tabulky

Tabulka `mereni_doma` ma sloupce:
- `tcas` (TEXT, defaultne se doplni automaticky)
- `druh_mereni` (TEXT)
- `hodnota` (REAL)

Interni sloupec `id` je primarni klic pro snadne razeni a identifikaci zaznamu.

## 7) Co zkusit dal

- pridej filtr podle typu mereni,
- pridej validaci povoleneho rozsahu `hodnota`,
- pridej endpoint pro mazani dat.

## 8) Uzitecne odkazy

- Oficialni dokumentace FastAPI: https://fastapi.tiangolo.com/
