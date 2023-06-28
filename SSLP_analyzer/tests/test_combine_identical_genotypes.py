from SSLP_App.utils import read_haplotypes,extract_sslps,generate_all_combinations,combine_identical_genotypes
import pytest

def test_combine_identical_genotypes_empty_input_raises_IndexError():
    try:
        combine_identical_genotypes([])
    except Exception as e:
        assert isinstance(e,IndexError)
    else:
        pytest.fail("Error not raised when expected")
        
def test_combine_identical_genotypes_wrong_input_type_raises_TypeError():
    try:
        combine_identical_genotypes("Wrong input type")
    except Exception as e:
        assert isinstance(e,TypeError)
    else:
        pytest.fail("Error not raised when expected")
        
def test_combine_identical_genotypes_list_too_short_raises_UnboundLocalError():
    try:
        combine_identical_genotypes([0])
    except Exception as e:
        assert isinstance(e,UnboundLocalError)
    else:
        pytest.fail("Error not raised when expected")