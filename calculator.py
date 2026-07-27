from __future__ import annotations


def calculate_cfe_cost(
    energy_kwh: float,
    tariff_data: dict,
    dap_amount: float = 0.0
) -> dict:
    """
    Calculate CFE energy cost.

    Args:
        energy_kwh:
            Total energy consumed in kWh.

        tariff_data:
            Loaded tariff JSON.

        dap_amount:
            Fixed DAP amount.

    Returns:
        Dictionary with cost breakdown.
    """

    remaining_energy = energy_kwh

    energy_cost = 0.0

    blocks_used = []


    for block in tariff_data.get(
        "blocks",
        []
    ):

        limit = block["limit"]

        price = block["price"]


        if remaining_energy <= 0:
            break


        # Unlimited block
        if limit == -1:

            consumed = remaining_energy


        else:

            consumed = min(
                remaining_energy,
                limit
            )


        block_cost = (
            consumed *
            price
        )


        energy_cost += block_cost


        blocks_used.append(
            {
                "name": block["name"],
                "energy": consumed,
                "price": price,
                "cost": block_cost
            }
        )


        remaining_energy -= consumed



    # IVA

    iva_rate = (
        tariff_data
        .get("charges", {})
        .get("iva", 0)
    )


    iva = (
        energy_cost *
        iva_rate
    )


    # DAP

    dap = 0

    if (
        tariff_data
        .get("charges", {})
        .get("dap", False)
    ):

        dap = dap_amount



    total = (
        energy_cost +
        iva +
        dap
    )


    return {

        "energy_kwh": energy_kwh,

        "energy_cost": round(
            energy_cost,
            2
        ),

        "iva": round(
            iva,
            2
        ),

        "dap": round(
            dap,
            2
        ),

        "total": round(
            total,
            2
        ),

        "blocks": blocks_used
    }
