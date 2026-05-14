from __future__ import annotations

import html
import sqlite3
from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# Cesta k SQLite databazi v koreni projektu.
DB_PATH = Path("data.db")

app = FastAPI(title="Jednoducha FastAPI + SQLite aplikace")


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
    """Vytvori tabulku a pripadne provede jednoduchou migraci nazvu sloupce."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS mereni (
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


@app.post("/mereni")
def uloz_mereni(vstup: MereniVstup) -> dict:
    """Prijme JSON data a ulozi je do tabulky `mereni`."""
    with get_connection() as conn:
        if vstup.tcas is None:
            # Pokud cas neprisel, nechame databazi doplnit default hodnotu.
            cursor = conn.execute(
                'INSERT INTO mereni (druh_mereni, hodnota) VALUES (?, ?)',
                (vstup.druh_mereni, vstup.hodnota),
            )
        else:
            cursor = conn.execute(
                'INSERT INTO mereni (tcas, druh_mereni, hodnota) VALUES (?, ?, ?)',
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


@app.get("/api/mereni")
def api_mereni(druh_mereni: Optional[str] = None) -> list[dict]:
    """Vrati data z tabulky `mereni` jako JSON.

    Pokud je zadany query parametr `druh_mereni`, vrati pouze odpovidajici zaznamy.
    """
    with get_connection() as conn:
        if druh_mereni:
            rows = conn.execute(
                """
                SELECT id, tcas, druh_mereni, hodnota
                FROM mereni
                WHERE druh_mereni = ?
                ORDER BY id DESC
                """,
                (druh_mereni,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, tcas, druh_mereni, hodnota FROM mereni ORDER BY id DESC"
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


@app.get("/prehled", response_class=HTMLResponse)
def prehled_mereni() -> str:
    """Vrati jednoduchou HTML stranku s obsahem tabulky `mereni`."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, tcas, druh_mereni, hodnota FROM mereni ORDER BY id DESC"
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
        "  <p>Endpoint pro vlozeni dat: <code>POST /mereni</code></p>",
        "  <p>JSON API: <code>GET /api/mereni</code></p>",
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
