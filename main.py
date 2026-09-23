import os
import json
import shutil
import time

from playwright.sync_api import sync_playwright

from scraper import (
    get_competitions,
    get_matches,
    get_match_details
)

from ics_generator import generate_ics
from output import save_json


with open(
    "teams.json",
    encoding="utf-8"
) as f:

    teams = json.load(f)["teams"]


with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir="playwright_profile",
        headless=False,
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/139.0.0.0 Safari/537.36"
        )
    )
    page.add_init_script("""
    Object.defineProperty(
        navigator,
        'webdriver',
        {
            get: () => undefined
        }
    )
    """)
    page.set_viewport_size({
        "width": 1920,
        "height": 1080
    })
    page.set_extra_http_headers({
        "Accept-Language": "ca-ES,ca;q=0.9,es;q=0.8"
    })
    os.makedirs(
        "docs",
        exist_ok=True
    )
    for team in teams:
        time.sleep(3)
        team_id = team["id"]
        team_name = team["name"]

        print()
        print(f"Equip: {team_name}")

        competitions = get_competitions(
            page,
            team_id
        )

        all_matches = []

        for competition in competitions:

            match_ids = get_matches(
                page,
                competition
            )

            for match_id in match_ids:

                details = get_match_details(
                    page,
                    match_id
                )

                if team_name in (
                    details["home"]
                    + details["away"]
                ):

                    all_matches.append(
                        details
                    )

        # Eliminació de duplicats
        unique_matches = {}

        for match in all_matches:
            unique_matches[
                match["match_id"]
            ] = match

        all_matches = list(
            unique_matches.values()
        )

        print(
            f"Partits trobats per {team_name}: {len(all_matches)}"
        )
        if len(all_matches) == 0:
            raise Exception(
                "No s'han trobat partits. Possible reCAPTCHA."
            )
        json_file = save_json(
            team_id,
            all_matches
        )

        print(
            "JSON generat:",
            json_file
        )

        ics_file = generate_ics(
            team_id,
            team_name,
            all_matches
        )

        print(
            "ICS generat:",
            ics_file
        )
        shutil.copy(
            ics_file,
            f"docs/{team_id}.ics"
        )

        print(
            f"Copiat a docs/{team_id}.ics"
        )

    context.close()