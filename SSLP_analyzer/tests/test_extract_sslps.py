from SSLP_App.utils import read_haplotypes,extract_sslps
import pytest
import os

def test_extract_sslps_empty_selection_empty_result():
    os.environ["DATABASE_JSON_FILE"] = "haplotypes.json"
    returnvalue = extract_sslps([],read_haplotypes("European"))
    assert returnvalue == ([],[])

def test_extract_sslps_invalid_selection_empty_result():
    os.environ["DATABASE_JSON_FILE"] = "haplotypes.json"
    returnvalue = extract_sslps([-10,-10,-10,-10],read_haplotypes("European"))
    assert returnvalue == ([],[])


def test_extract_sslps_valid_input_return_chr_lists():
    os.environ["DATABASE_JSON_FILE"] = "haplotypes.json"
    
    try:
        returnvalue = extract_sslps([161,162,163,164],read_haplotypes("European"))
    except Exception as e:
        pytest.fail(f"Exception raised when not expected {e}")
    assert isinstance(returnvalue,tuple)
    chr4,chr10 = returnvalue
    assert isinstance(chr4,list)
    assert isinstance(chr10,list)
    
    
