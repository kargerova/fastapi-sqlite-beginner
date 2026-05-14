from __future__ import annotations

import html
import json
import sqlite3
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Cesta k SQLite databazi v koreni projektu.
DB_PATH = Path("data.db")

app = FastAPI(title="Jednoducha FastAPI + SQLite aplikace")
templates = Jinja2Templates(directory="templates")


class MereniVstup(BaseModel):
    """Datovy model pro vstupni JSON s merenim.

    Poznamka:
    - `tcas` je nepovinny. Pokud neprijde, doplni ho databaze automaticky.
    """

    tcas: Optional[str] = None
    druh_mereni: str
    hodnota: float


def get_connection() -> sqlite3.Connection:
    """Vytvori pripojeni do SQLite a nastavi vraceni radku jako slovnik."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Vytvori tabulku/tabulky."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS mereni_doma (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tcas TEXT DEFAULT (datetime('now', 'localtime')),
                druh_mereni TEXT NOT NULL,
                hodnota REAL NOT NULL
            )
            """
        )

        # Pro ukazku mame i druhou tabulku, ale zatim ji nepouzivame.
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS mereni_zahrada (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tcas TEXT DEFAULT (datetime('now', 'localtime')),
                druh_mereni TEXT NOT NULL,
                hodnota REAL NOT NULL
            )
            """
        )

        conn.commit()


# Pri startu aplikace zajistime existenci tabulky.
init_db()


@app.post("/mereni_doma")
def uloz_mereni(vstup: MereniVstup) -> dict:
    """Prijme JSON data a ulozi je do tabulky `mereni_doma`."""
    with get_connection() as conn:
        if vstup.tcas is None:
            # Pokud cas neprisel, nechame databazi doplnit default hodnotu.
            cursor = conn.execute(
                'INSERT INTO mereni_doma (druh_mereni, hodnota) VALUES (?, ?)',
                (vstup.druh_mereni, vstup.hodnota),
            )
        else:
            cursor = conn.execute(
                'INSERT INTO mereni_doma (tcas, druh_mereni, hodnota) VALUES (?, ?, ?)',
                (vstup.tcas, vstup.druh_mereni, vstup.hodnota),
            )

        conn.commit()

    return {
        "status": "ok",
        "id": cursor.lastrowid,
        "ulozeno": {
            "tcas": vstup.tcas,
            "druh_mereni": vstup.druh_mereni,
            "hodnota": vstup.hodnota,
        },
    }


@app.get("/mereni_doma")
def api_mereni(druh_mereni: Optional[str] = None) -> list[dict]:
    """Vrati data z tabulky `mereni_doma` jako JSON.

    Pokud je zadany query parametr `druh_mereni`, vrati pouze odpovidajici zaznamy.
    """
    with get_connection() as conn:
        if druh_mereni:
            rows = conn.execute(
                """
                SELECT id, tcas, druh_mereni, hodnota
                FROM mereni_doma
                WHERE druh_mereni = ?
                ORDER BY id DESC
                """,
                (druh_mereni,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, tcas, druh_mereni, hodnota FROM mereni_doma ORDER BY id DESC"
            ).fetchall()

    return [
        {
            "id": row["id"],
            "tcas": row["tcas"],
            "druh_mereni": row["druh_mereni"],
            "hodnota": row["hodnota"],
        }
        for row in rows
    ]


@app.get("/mereni_doma_prehled", response_class=HTMLResponse)
def prehled_mereni() -> str:
    """Vrati jednoduchou HTML stranku s obsahem tabulky `mereni_doma`."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, tcas, druh_mereni, hodnota FROM mereni_doma ORDER BY id DESC"
        ).fetchall()

    # Jednoducha HTML sablona vytvorena jako string, aby byl priklad co nejprehlednejsi.
    lines = [
        "<!doctype html>",
        "<html lang='cs'>",
        "<head>",
        "  <meta charset='utf-8' />",
        "  <meta name='viewport' content='width=device-width, initial-scale=1' />",
        "  <title>Prehled mereni</title>",
        "  <style>",
        "    body { font-family: sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; }",
        "    table { border-collapse: collapse; width: 100%; }",
        "    th, td { border: 1px solid #d0d7de; padding: 0.5rem; text-align: left; }",
        "    th { background: #f6f8fa; }",
        "    h1 { margin-bottom: 0.75rem; }",
        "  </style>",
        "</head>",
        "<body>",
        "  <h1>Prehled mereni</h1>",
        "  <p>Endpoint pro vlozeni dat: <code>POST /mereni_doma</code></p>",
        "  <p>JSON API: <code>GET /mereni_doma</code></p>",
        "  <table>",
        "    <thead><tr><th>ID</th><th>tcas</th><th>druh_mereni</th><th>hodnota</th></tr></thead>",
        "    <tbody>",
    ]

    for row in rows:
        lines.append(
            "      <tr>"
            f"<td>{row['id']}</td>"
            f"<td>{html.escape(str(row['tcas']))}</td>"
            f"<td>{html.escape(str(row['druh_mereni']))}</td>"
            f"<td>{row['hodnota']}</td>"
            "</tr>"
        )

    if not rows:
        lines.append("      <tr><td colspan='4'><em>Zatim bez dat.</em></td></tr>")

    lines.extend(["    </tbody>", "  </table>", "</body>", "</html>"])
    return "\n".join(lines)


@app.get("/mereni_doma_prehled2", response_class=HTMLResponse)
def prehled_mereni_sablona(request: Request):
    """Vrati HTML stranku renderovanou ze sablony."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, tcas, druh_mereni, hodnota FROM mereni_doma ORDER BY id DESC"
        ).fetchall()

    return templates.TemplateResponse(
        "mereni_doma_prehled2.html",
        {
            "request": request,
            "rows": rows,
        },
    )


@app.get("/mereni_doma_graf", response_class=HTMLResponse)
def graf_mereni_doma(request: Request, druh_mereni: str):
    """Vrati jednoduchy graf hodnot v case podle druhu mereni."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT tcas, hodnota
            FROM mereni_doma
            WHERE druh_mereni = ?
            ORDER BY tcas ASC, id ASC
            """,
            (druh_mereni,),
        ).fetchall()

    labels = [str(row["tcas"]) for row in rows]
    values = [float(row["hodnota"]) for row in rows]

    return templates.TemplateResponse(
        "mereni_doma_graf.html",
        {
            "request": request,
            "druh_mereni": druh_mereni,
            # Predame data uz jako JSON stringy, aby je slo snadno nacist v JavaScriptu.
            "labels_json": json.dumps(labels, ensure_ascii=False),
            "values_json": json.dumps(values),
            "count": len(rows),
        },
    )
