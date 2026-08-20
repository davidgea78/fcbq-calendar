import re
from bs4 import BeautifulSoup


def get_competitions(page, team_id):

    page.goto(
        f"https://www.basquetcatala.cat/equip/{team_id}"
    )

    page.wait_for_timeout(5000)

    html = page.content()
    if "Verificació de seguretat" in html:
        print("RECAPTCHA A EQUIP")

    return sorted(
        set(
            re.findall(
                r"resultats/(\d+)",
                html
            )
        )
    )


def get_matches(page, competition_id):
    page.goto(
        f"https://www.basquetcatala.cat/competicions/resultats/{competition_id}/0"
    )

    page.wait_for_timeout(5000)

    html = page.content()

    with open(
        f"competicio_{competition_id}.html",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(html)

    return sorted(
        set(
            re.findall(
                r"llistatpartits/(\d+)",
                html
            )
        )
    )

def get_match_details(page, match_id):

    page.goto(
        f"https://www.basquetcatala.cat/partits/llistatpartits/{match_id}"
    )

    page.wait_for_timeout(3000)

    html = page.content()

    if "Verificació de seguretat" in html:
        print("RECAPTCHA DETECTAT")

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    text = soup.get_text(
        "\n",
        strip=True
    )

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    data = ""
    hora = ""
    competicio = ""
    grup = ""
    venue = ""

    for i, line in enumerate(lines):

        if line == "Competició:" and i + 1 < len(lines):
            competicio = lines[i + 1]

        if line == "Grup:" and i + 1 < len(lines):
            grup = lines[i + 1]

        if line == "Data partit:" and i + 1 < len(lines):
            data = lines[i + 1]

        if line == "Hora partit:" and i + 1 < len(lines):
            hora = lines[i + 1]

        if line == "Instal·lació:" and i + 2 < len(lines):
            venue = (
                lines[i + 1]
                + "\n"
                + lines[i + 2]
            )

    idx_local = lines.index("Local")

    home = lines[idx_local + 2]
    away = lines[idx_local + 3]
    idx_local = lines.index("Local")
    return {
        "match_id": match_id,
        "competition": competicio,
        "group": grup,
        "date": data,
        "time": hora,
        "venue": venue,
        "home": home,
        "away": away
    }