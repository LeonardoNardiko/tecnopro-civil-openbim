# TecnoPRO Civil & OpenBIM Normative Suite

[![CI](https://github.com/LeonardoNardiko/tecnopro-civil-openbim/actions/workflows/ci.yml/badge.svg)](https://github.com/LeonardoNardiko/tecnopro-civil-openbim/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776ab.svg)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/License-MIT-0ea5e9.svg)](LICENSE)
[![Hub: civil.tecnopro.me](https://img.shields.io/badge/OpenBIM_Hub-civil.tecnopro.me-e67e22.svg)](https://civil.tecnopro.me)

Auditable Python verification benchmarks and open construction data serializers backing **[TecnoPRO Civil](https://civil.tecnopro.me)** — an engineering hub focused on structural design, geotechnical foundations, constraint-based floor planning (`CP-SAT`), and OpenBIM (`IFC4` / `FIEBDC-3`).

---

## Covered Engineering Modules

| Module | Standard / Spec | Capabilities | Production Integration |
| :--- | :--- | :--- | :--- |
| **Geotechnical Foundations** | `ABNT NBR 6122` (*Décourt-Quaresma*) | Axial tip & lateral shaft bearing capacity from meter-by-meter $N_{\text{SPT}}$ blow profiles with partial safety checks | [civil.tecnopro.me](https://civil.tecnopro.me) |
| **Structural Wind Actions** | `ABNT NBR 6123` | Characteristic wind velocity $V_k$ and dynamic pressure $q = 0.613 V_k^2$ for industrial steel sheds, packing houses & high-tech greenhouses ($V_0 = 45\text{ m/s}$ São Paulo inland benchmark) | [civil.tecnopro.me](https://civil.tecnopro.me) |
| **Open Cost Interchange** | `FIEBDC-3 (.bc3)` | Native open budget serializer compatible with **CYPE Arquimedes**, **Presto**, and SINAPI/OpenBIM quantity takeoffs | **TecnoBIM v2** |

---

## Quick Verification

Zero third-party packages required to run the baseline verification suite:

```bash
git clone https://github.com/LeonardoNardiko/tecnopro-civil-openbim.git
cd tecnopro-civil-openbim
python -m unittest discover -s tests -v
```

---

## Author & Legal Engineering Sign-off

**Leonardo de Lima Junior (Leonardo Nardiko)**  
B.Sc. in Civil Engineering (**Active CREA-SP**) · Lean Six Sigma Black Belt (`#111524`) · 2x MBA  
🌐 Executive Portfolio: [nardiko.me](https://nardiko.me) · 🏗️ Civil & BIM Hub: [civil.tecnopro.me](https://civil.tecnopro.me) · ⚙️ Mechanical Suite: [tecnopro.me](https://tecnopro.me)
