import json
from pathlib import Path


TARIFF_PATH = Path(__file__).parent



def load_tariff(
    country: str,
    tariff: str
):

    file = (
        TARIFF_PATH
        / country.lower()
        / f"{tariff.lower()}.json"
    )


    if not file.exists():

        raise FileNotFoundError(
            f"Tariff not found: {file}"
        )


    with open(
        file,
        "r",
        encoding="utf-8"
    ) as tariff_file:

        return json.load(
            tariff_file
        )
