from SSLP_App.utils import read_haplotypes,extract_sslps
import os
import pytest

def test_extract_sslps_empty_selection_empty_result():
    returnvalue = extract_sslps([],read_haplotypes("European"))
    assert returnvalue == ([],[])

def test_extract_sslps_invalid_selection_empty_result():
    returnvalue = extract_sslps([-10,-10,-10,-10],read_haplotypes("European"))
    assert returnvalue == ([],[])
