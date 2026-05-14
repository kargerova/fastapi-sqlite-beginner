# Co je FastAPI (pro zacatecniky)

FastAPI je moderni Python framework pro tvorbu webovych API.
Je popularni, protoze je:
- rychly,
- jednoduche se v nem pise,
- automaticky generuje dokumentaci,
- dobre spolupracuje s typy v Pythonu.

## Jak si FastAPI predstavit

FastAPI je "vratny" pro tvoji aplikaci:
- prijme HTTP pozadavek (napr. GET nebo POST),
- preda data do tve funkce,
- vrati odpoved klientovi (JSON nebo HTML).

V tomto projektu mas napriklad:
- `POST /mereni` pro ulozeni dat,
- `GET /api/mereni` pro vraceni dat jako JSON,
- `GET /prehled` pro zobrazeni dat v HTML.

## Proc je FastAPI dobre pro vyuku

- Ucis se rovnou prakticke API endpointy.
- Vidis jasnou vazbu mezi kodem a HTTP.
- Pydantic modely pomahaji kontrolovat vstupni data.

## /docs - vestavena dokumentace

Po spusteni aplikace otevri:

- http://127.0.0.1:8000/docs

Toto je interaktivni dokumentace, kde muzes endpointy rovnou testovat.
Je to skvely nastroj pro zacatecniky.

## Nejmensi pracovni postup

1. Spust server (`uvicorn app:app --reload`).
2. Otevri `/docs`.
3. Vyzkousej `POST /mereni` s JSON daty.
4. Otevri `GET /api/mereni` a `GET /prehled`.

## Dalsi krok

Az budes mit zaklady, zkus pridat:
- validaci hodnot,
- filtraci v API,
- mazani nebo upravu zaznamu.
