"""
TecnoPRO Civil & OpenBIM Normative Reference Benchmarks
Public analytical baseline & open data interchange utilities backing https://civil.tecnopro.me

Modules covered:
1. ABNT NBR 6122 (Décourt-Quaresma): Pile bearing capacity from SPT blow counts (N_SPT)
2. ABNT NBR 6123: Dynamic wind pressure on industrial sheds & agricultural greenhouses
3. FIEBDC-3 (.bc3): Open construction cost-estimating interchange serializer (CYPE / Arquimedes / Presto)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
import math


# Décourt-Quaresma characteristic soil adhesion factor K (kPa) and alpha/beta coefficients
DECOURT_K_KPA = {
    "clay": 120.0,
    "silty_clay": 200.0,
    "sandy_silt": 250.0,
    "sand": 400.0,
}


@dataclass(frozen=True)
class PileCapacityResult:
    diameter_m: float
    length_m: float
    tip_area_m2: float
    perimeter_m: float
    q_tip_kn: float
    q_shaft_kn: float
    q_ult_kn: float
    q_adm_kn: float


def calc_spt_pile_decourt_quaresma(
    diameter_m: float,
    nspt_profile_1m: Sequence[int],
    soil_type: str = "silty_clay",
    alpha: float = 1.0,
    beta: float = 1.0,
) -> PileCapacityResult:
    """
    Computes ultimate and allowable axial bearing capacity of a bored/cast-in-place pile
    using the classic Décourt-Quaresma formulation referenced in Brazilian geotechnical practice (NBR 6122).
    `nspt_profile_1m` contains N_SPT readings at each 1.0 m depth interval down to pile tip.
    """
    if soil_type not in DECOURT_K_KPA:
        raise ValueError(f"Unsupported soil_type: {soil_type}")
    if len(nspt_profile_1m) < 3:
        raise ValueError("At least 3 meters of SPT profile are required.")

    length_m = float(len(nspt_profile_1m))
    tip_area_m2 = (math.pi / 4.0) * (diameter_m ** 2)
    perimeter_m = math.pi * diameter_m

    # Tip N_p: average of tip level, 1m above and 1m below (clamped to available profile)
    np_avg = sum(nspt_profile_1m[-3:]) / 3.0
    k_kpa = DECOURT_K_KPA[soil_type]
    q_tip_kn = alpha * k_kpa * np_avg * tip_area_m2

    # Lateral shaft N_l: clamp [3, 50] along shaft excluding tip neighborhood
    shaft_blows = [min(max(float(n), 3.0), 50.0) for n in nspt_profile_1m[:-1]]
    nl_avg = sum(shaft_blows) / len(shaft_blows)
    qs_kpa = 10.0 * (nl_avg / 3.0 + 1.0)
    q_shaft_kn = beta * qs_kpa * perimeter_m * (length_m - 1.0)

    q_ult_kn = q_tip_kn + q_shaft_kn
    # Décourt-Quaresma partial safety formulation: Q_adm = min(Q_ult / 2.0, Q_shaft / 1.3 + Q_tip / 4.0)
    q_adm_kn = min(q_ult_kn / 2.0, (q_shaft_kn / 1.3) + (q_tip_kn / 4.0))

    return PileCapacityResult(
        diameter_m=diameter_m,
        length_m=length_m,
        tip_area_m2=tip_area_m2,
        perimeter_m=perimeter_m,
        q_tip_kn=q_tip_kn,
        q_shaft_kn=q_shaft_kn,
        q_ult_kn=q_ult_kn,
        q_adm_kn=q_adm_kn,
    )


def calc_wind_pressure_nbr6123(
    v0_ms: float = 45.0,
    s1: float = 1.0,
    s2_b: float = 1.00,
    s2_p: float = 0.085,
    height_z_m: float = 8.0,
    s3: float = 1.0,
) -> dict[str, float]:
    """
    ABNT NBR 6123 characteristic wind speed V_k and dynamic pressure q (Pa and kN/m2).
    Default V0 = 45 m/s represents São Paulo inland industrial/agricultural belt
    (Campinas, Holambra, Artur Nogueira, Engenheiro Coelho).
    """
    if v0_ms <= 0 or height_z_m <= 0:
        raise ValueError("Wind speed V0 and height z must be positive.")
    s2 = s2_b * ((height_z_m / 10.0) ** s2_p)
    vk_ms = v0_ms * s1 * s2 * s3
    q_pa = 0.613 * (vk_ms ** 2)
    return {
        "v0_ms": v0_ms,
        "s1": s1,
        "s2": s2,
        "s3": s3,
        "vk_ms": vk_ms,
        "q_pa": q_pa,
        "q_kn_m2": q_pa / 1000.0,
    }


def export_fiebdc3_bc3(project_code: str, project_title: str, items: Sequence[dict]) -> str:
    """
    Generates a compliant FIEBDC-3 (.bc3) text stream for open BIM / SINAPI cost interchange
    with Arquimedes (CYPE), Presto and OpenBIM quantity takeoff tools.
    Each item dict expects: {'code': str, 'unit': str, 'summary': str, 'price': float, 'qty': float}.
    """
    lines = [
        "~V|TecnoPRO Civil OpenBIM|FIEBDC-3/2020|TecnoPRO 1.0||ANSI|",
        f"~K|\\2\\2\\3\\2\\2\\2\\2\\BRL\\",
        f"~C|{project_code}##||{project_title}|0|051126|0|",
    ]
    decomp_parts = []
    total_cost = 0.0
    for it in items:
        code = it["code"]
        unit = it["unit"]
        summary = it["summary"]
        price = float(it["price"])
        qty = float(it["qty"])
        total_cost += price * qty
        lines.append(f"~C|{code}|{unit}|{summary}|{price:.2f}|051126|0|")
        decomp_parts.append(f"{code}\\{qty:.3f}\\1\\")
    if decomp_parts:
        lines.append(f"~D|{project_code}##|" + "".join(decomp_parts) + "|")
    # Patch root budget total
    lines[2] = f"~C|{project_code}##||{project_title}|{total_cost:.2f}|051126|0|"
    return "\n".join(lines) + "\n"
