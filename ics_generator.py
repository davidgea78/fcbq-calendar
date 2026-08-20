from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from icalendar import Calendar, Event

def generate_ics(team_id, team_name, matches):

    cal = Calendar()

    for match in matches:

        if not match["date"]:
            continue

        dt = datetime.strptime(
            f"{match['date']} {match['time']}",
            "%d-%m-%Y %H:%M"
        ).replace(
            tzinfo=ZoneInfo("Europe/Madrid")
        )

        event = Event()

        event.add(
            "summary",
            f"PROVA HORA | {match['home']} - {match['away']}"
        )

        event.add(
            "dtstart",
            dt
        )
        event.add(
            "dtend",
            dt + timedelta(hours=2)
        )
        event.add(
            "location",
            match["venue"]
        )

        event.add(
            "description",
            (
                f"Competició: {match['competition']}\n"
                f"Grup: {match['group']}\n"
                f"Partit: {match['match_id']}\n"
                f"\n"
                f"Local: {match['home']}\n"
                f"Visitant: {match['away']}\n"
                f"\n"
                f"Ubicació:\n"
                f"{match['venue']}"
            )
        )

        event.add(
            "uid",
            f"fcbq-{match['match_id']}@calendar"
        )

        cal.add_component(event)

    filename = f"output/{team_id}.ics"

    with open(
        filename,
        "wb"
    ) as f:

        f.write(
            cal.to_ical()
        )

    return filename