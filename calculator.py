from __future__ import annotations



def calculate_cfe_cost(
    energy_kwh: float,
    tariff_data: dict,
    dap_amount: float = 0.0
) -> dict:
    """
    Calcula el costo estimado de energía CFE.

    energy_kwh:
        Consumo del periodo en kWh

    tariff_data:
        Archivo JSON de tarifa

    dap_amount:
        Cargo DAP fijo
    """


    remaining = energy_kwh


    energy_cost = 0.0


    blocks_used = []



    for block in tariff_data.get(
        "blocks",
        []
    ):


        if remaining <= 0:

            break



        limit = block.get(
            "limit",
            -1
        )


        price = block.get(
            "price",
            0
        )



        if limit == -1:

            consumed = remaining


        else:

            consumed = min(
                remaining,
                limit
            )



        cost = round(
            consumed * price,
            2
        )



        energy_cost += cost



        blocks_used.append(

            {

                "name":
                    block.get(
                        "name",
                        ""
                    ),

                "energy":
                    round(
                        consumed,
                        2
                    ),

                "price":
                    price,

                "cost":
                    cost

            }

        )



        remaining -= consumed






    #
    # IVA
    #

    iva = 0


    if tariff_data.get(
        "charges",
        {}
    ).get(
        "iva",
        False
    ):


        iva_rate = tariff_data.get(
            "charges",
            {}
        ).get(
            "iva_rate",
            0.16
        )


        iva = energy_cost * iva_rate







    #
    # DAP
    #

    dap = 0



    if tariff_data.get(
        "charges",
        {}
    ).get(
        "dap",
        False
    ):


        dap = dap_amount







    total = (

        energy_cost +

        iva +

        dap

    )






    return {


        "energy_kwh":

            round(
                energy_kwh,
                2
            ),



        "energy_cost":

            round(
                energy_cost,
                2
            ),



        "iva":

            round(
                iva,
                2
            ),



        "dap":

            round(
                dap,
                2
            ),



        "total":

            round(
                total,
                2
            ),



        "blocks":

            blocks_used

    }
