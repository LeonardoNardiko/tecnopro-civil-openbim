import unittest
from tecnopro_civil import (
    calc_spt_pile_decourt_quaresma,
    calc_wind_pressure_nbr6123,
    export_fiebdc3_bc3,
)


class TestCivilOpenBimBenchmarks(unittest.TestCase):
    def test_spt_pile_decourt_quaresma(self):
        # 40 cm bored pile, 8m deep in silty clay (N_SPT progressive 4..18)
        profile = [4, 5, 7, 8, 10, 13, 16, 18]
        res = calc_spt_pile_decourt_quaresma(0.40, profile, soil_type="silty_clay")
        self.assertAlmostEqual(res.length_m, 8.0)
        self.assertGreater(res.q_tip_kn, 350.0)
        self.assertGreater(res.q_shaft_kn, 300.0)
        self.assertLess(res.q_adm_kn, res.q_ult_kn / 1.99)
        self.assertGreater(res.q_adm_kn, 300.0)

    def test_wind_pressure_nbr6123_sp_inland(self):
        # Holambra / Artur Nogueira / Campinas industrial shed or high-tech greenhouse (V0 = 45 m/s, z = 8m)
        w = calc_wind_pressure_nbr6123(v0_ms=45.0, s1=1.0, s2_b=1.0, s2_p=0.085, height_z_m=8.0, s3=1.0)
        self.assertAlmostEqual(w["s2"], (8.0 / 10.0) ** 0.085, places=5)
        self.assertGreater(w["vk_ms"], 43.5)
        self.assertAlmostEqual(w["q_pa"], 0.613 * (w["vk_ms"] ** 2), places=3)
        self.assertGreater(w["q_kn_m2"], 1.15)

    def test_export_fiebdc3_bc3_format(self):
        bc3 = export_fiebdc3_bc3(
            project_code="SHED01",
            project_title="Galpao Estrutural Metalico 600m2",
            items=[
                {"code": "SINAPI_ACO", "unit": "kg", "summary": "Perfil Aco ASTM A572 Gr50", "price": 14.50, "qty": 12000},
                {"code": "SINAPI_CONC", "unit": "m3", "summary": "Concreto Estrutural fck 30MPa", "price": 520.00, "qty": 45},
            ],
        )
        self.assertIn("~V|TecnoPRO Civil OpenBIM|FIEBDC-3/2020|", bc3)
        self.assertIn("~C|SHED01##||Galpao Estrutural Metalico 600m2|197400.00|", bc3)
        self.assertIn("~D|SHED01##|SINAPI_ACO\\12000.000\\1\\SINAPI_CONC\\45.000\\1\\|", bc3)


if __name__ == "__main__":
    unittest.main()
