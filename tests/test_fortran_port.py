import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from kesten.fortran_port import conc_port, lqvp_port, param_port


class TestFortranPortHelpers(unittest.TestCase):
    def test_conc_port_returns_nonnegative_components(self) -> None:
        c1, c2, c3, c4 = conc_port(
            temp=820.0,
            pressure=100.0,
            wm4=32.045,
            wm3=17.031,
            wm2=28.0134,
            wm1=2.016,
            gas_constant=10.7316,
            h=715.478,
            hf=0.0,
        )
        self.assertGreaterEqual(c1, 0.0)
        self.assertGreaterEqual(c2, 0.0)
        self.assertGreaterEqual(c3, 0.0)
        self.assertGreaterEqual(c4, 0.0)

    def test_param_port_deterministic(self) -> None:
        first = param_port(
            temp=900.0,
            z=0.02,
            cc=0.1,
            hr=-1900.0,
            lvop=0,
            z0=0.0,
            g0=3.0,
            fc=0.0,
            gatz0=3.0,
            agm=2500.0,
            bgm=50000.0,
            alpha1=1.0e10,
            alpha2=1.0e11,
            dif3=0.17e-3,
            dif4=0.95e-4,
            pressure=100.0,
            kp=0.4e-4,
            c1=0.01,
        )
        second = param_port(
            temp=900.0,
            z=0.02,
            cc=0.1,
            hr=-1900.0,
            lvop=0,
            z0=0.0,
            g0=3.0,
            fc=0.0,
            gatz0=3.0,
            agm=2500.0,
            bgm=50000.0,
            alpha1=1.0e10,
            alpha2=1.0e11,
            dif3=0.17e-3,
            dif4=0.95e-4,
            pressure=100.0,
            kp=0.4e-4,
            c1=0.01,
        )
        self.assertEqual(first, second)

    def test_lqvp_port_advances_to_or_toward_hv(self) -> None:
        z_values, h_values, wfv_values, _ = lqvp_port(
            h_start=212.628,
            z_start=7.37459e-4,
            deriv_start=100.0,
            dhdz_start=1.0e6,
            temp_vap=820.0,
            hl=212.628,
            hv=715.478,
            enmx2=40.0,
            max_steps=50,
            z0=0.0,
            g0=3.0,
            fc=0.0,
            gatz0=3.0,
            agm=2500.0,
            bgm=50000.0,
            alpha1=1.0e10,
            alpha2=1.0e11,
            dif3=0.17e-3,
            dif4=0.95e-4,
            pressure=100.0,
            kp=0.4e-4,
            c1=1.0,
        )
        self.assertGreater(len(z_values), 1)
        self.assertTrue(all(b > a for a, b in zip(z_values, z_values[1:])))
        self.assertGreaterEqual(h_values[-1], h_values[0])
        self.assertLessEqual(max(wfv_values), 1.0)


if __name__ == "__main__":
    unittest.main()
