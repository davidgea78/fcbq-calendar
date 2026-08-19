import json


def save_json(team_id, matches):

    filename = f"output/{team_id}.json"

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            matches,
            f,
            indent=2,
            ensure_ascii=False
        )

    return filename