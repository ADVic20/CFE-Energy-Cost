from __future__ import annotations

import json
from pathlib import Path


BASE_PATH = Path(__file__).parent / "tariffs"



def load_tariff(
    tariff: str,
    region: str,
) -> dict:


    tariff = tariff.lower()


    filename_map = {

        "1":
            "tarifa_1.json",

        "1a":
            "tarifa_1a.json",

        "1b":
            "tarifa_1b.json",

        "1c":
            "tarifa_1c.json",

        "dac":
            "dac.json",

    }


    filename = filename_map.get(
        tariff
    )


    if filename is None:

        return {}



    path = (

        BASE_PATH

        / "mexico"

        / region.lower()

        / filename

    )


    if not path.exists():

        return {}



    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)
