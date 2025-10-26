# test_phases.py - Testes unitários pros fits
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from greek_phases import friedmann_with_tau
import numpy as np
import pytest

def test_friedmann_tau():
    a, t = 1.0, 0.0
    H = friedmann_with_tau(a, t, tau=0.042)
    assert H > 1.0  # H base deve ser >1 no early universe
    assert np.isclose(H, np.sqrt((8*np.pi/3) + 1/3 + 0.215*1.618 + 0.042), rtol=0.01)

if __name__ == '__main__':
    pytest.main([__file__])
