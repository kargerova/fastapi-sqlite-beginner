# Co je SQLite (pro zacatecniky)

SQLite je mala relacni databaze ulozena v jednom souboru (napr. `data.db`).
Nemusi bezet zadny databazovy server.
To je idealni pro vyuku, prototypy a mensi aplikace.

## Zakladni pojmy

- databaze: soubor s daty (`data.db`)
- tabulka: misto, kde jsou zaznamy (napr. `mereni`)
- radek: jeden zaznam
- sloupec: jedna vlastnost zaznamu (`tcas`, `druh_mereni`, `hodnota`)

## Proc je SQLite vhodna pro zacatecniky

- Jednoducha instalace a pouziti.
- SQL se ucis na realnych datech.
- Vse je lokalne v jednom souboru.

## Jednoduche nastroje pro praci se SQLite

1. sqlite3 (prikazova radka)
- Zakladni CLI nastroj.
- Rychly na uceni SQL prikazu.
- Priklad spusteni: `sqlite3 data.db`

2. DB Browser for SQLite (graficky nastroj)
- Vhodny pro uplne zacatecniky.
- Umoznuje klikat tabulky, prohlizet data a poustet SQL dotazy.
- Web: https://sqlitebrowser.org/

3. DBeaver (univerzalni DB klient)
- Podporuje mnoho databazi vcetne SQLite.
- Hodi se, pokud chces casem prejit i na PostgreSQL/MySQL.
- Web: https://dbeaver.io/

## Zakladni SQL prikazy (rychly prehled)

- vytvoreni tabulky: `CREATE TABLE ...`
- vlozeni dat: `INSERT INTO ...`
- cteni dat: `SELECT ...`
- uprava dat: `UPDATE ...`
- smazani dat: `DELETE ...`

## Priklad dotazu pro tvuj projekt

```sql
SELECT id, tcas, druh_mereni, hodnota
FROM mereni
ORDER BY id DESC;
```

## Jak pracovat se SQLite v tomto projektu

1. Spust FastAPI aplikaci.
2. Posli data na `POST /mereni`.
3. Otevri `GET /api/mereni` nebo `GET /prehled`.
4. Databazovy soubor `data.db` si otevri v DB Browseru a prohledni tabulku `mereni`.

Timto se nauci srovnat, jak stejna data vypadaji:
- v API odpovedi,
- v HTML tabulce,
- primo v databazi.
