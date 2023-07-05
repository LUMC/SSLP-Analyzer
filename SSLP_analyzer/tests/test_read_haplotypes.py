from SSLP_App.utils import read_haplotypes
import os
import pytest


def test_read_haplotypes_valid_input_return_haplotypes():
    os.environ["DATABASE_JSON_FILE"] = "haplotypes.json"
    try:
        haplotypes = read_haplotypes("European")
    except Exception as e:
        pytest.fail(f"Exception raised: {e}")
    else:
        assert isinstance(haplotypes,dict)
        assert "chr4" in haplotypes
        assert "chr10" in haplotypes
        sslp = haplotypes["chr4"][list(haplotypes["chr4"].keys())[0]]
        assert isinstance(sslp,list)
        sslp = sslp[0]
        assert "haplotype" in sslp
        assert "%" in sslp
        assert "permissive" in sslp
        
def test_read_haplotypes_file_not_present_raises_FileNotFoundError():
    os.environ["DATABASE_JSON_FILE"] = "haplotypes.json"
    os.rename("haplotypes.json","temp.json")
    try:
        read_haplotypes("European")
    except Exception as e:
        assert isinstance(e,FileNotFoundError)
    else:
        pytest.fail("File found when it should not be found.")
    os.rename("temp.json","haplotypes.json")
    
def test_read_haplotypes_invalid_population_raises_KeyError():
    os.environ["DATABASE_JSON_FILE"] = "haplotypes.json"
    try:
        read_haplotypes("abc")
    except Exception as e:
        assert isinstance(e,KeyError)
    else:
        pytest.fail("Population should not be present in file!")
    
def test_read_haplotypes_wrong_input_type_raises_TypeError():
    os.environ["DATABASE_JSON_FILE"] = "haplotypes.json"
    try:
        read_haplotypes(["European"])
    except Exception as e:
        assert isinstance(e,TypeError)
    else:
        pytest.fail("Method accepted invalid parameters.")