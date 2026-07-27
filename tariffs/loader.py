from __future__ import annotations


import json

from pathlib import Path



BASE_PATH = Path(__file__).parent






def load_tariff(
    country: str,
    region: str,
    tariff: str
):


    filename = (
        f"{tariff.lower()}.json"
    )


    path = (

        BASE_PATH /

        country.lower() /

        region.lower() /

        filename

    )



    if not path.exists():

        return None




    try:


        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:


            return json.load(
                file
            )



    except Exception:


        return None
