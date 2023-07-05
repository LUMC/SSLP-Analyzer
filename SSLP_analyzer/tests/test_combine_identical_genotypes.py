from SSLP_App.utils import read_haplotypes,extract_sslps,generate_all_combinations,combine_identical_genotypes
import pytest

def check_unique(chances):
    for i,value in enumerate(chances):
        chances[i][1] = sorted(value[1])
    for i1,chance1 in enumerate(chances):
        for i2,chance2 in enumerate(chances):
            if i1 != i2:
                if chance1 == chance2:
                    return False
    else:
        return True
        

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
        
def test_combine_identical_genotypes_valid_input_returns_expected_values():
    population = "European"
    selection = [161,162,163,164]
    try:
        haplotypes = read_haplotypes(population)
        chr4_SSLPs, chr10_SSLPs = extract_sslps(selection,haplotypes)
        permissive_chance, total_permissive_chance = generate_all_combinations(selection,chr4_SSLPs,chr10_SSLPs)
        sorted_by_chance = sorted(permissive_chance, key = lambda x:x[0], reverse=True)
        combined_genotypes = combine_identical_genotypes(sorted_by_chance)
    except Exception as e:
        pytest.fail(f"Exception raised when not expected {e}")
    else:
        assert isinstance(combined_genotypes,list)
        assert isinstance(combined_genotypes[0],list)
        assert isinstance(combined_genotypes[0][0],float)
        assert isinstance(combined_genotypes[0][1],list)
        assert isinstance(combined_genotypes[0][2],int)
        assert isinstance(combined_genotypes[0][1][0],str)
        assert check_unique(sorted_by_chance)
        
def test_combine_identical_genotypes_input_not_sorted_returns_invalid_values():
    population = "European"
    selection = [161,162,163,164]
    try:
        haplotypes = read_haplotypes(population)
        chr4_SSLPs, chr10_SSLPs = extract_sslps(selection,haplotypes)
        permissive_chance, total_permissive_chance = generate_all_combinations(selection,chr4_SSLPs,chr10_SSLPs)
        combined_genotypes = combine_identical_genotypes(permissive_chance)
    except Exception as e:
        pytest.fail(f"Exception raised when not expected {e}")
    else:
        assert isinstance(combined_genotypes,list)
        assert isinstance(combined_genotypes[0],list)
        assert isinstance(combined_genotypes[0][0],float)
        assert isinstance(combined_genotypes[0][1],list)
        assert isinstance(combined_genotypes[0][2],int)
        assert isinstance(combined_genotypes[0][1][0],str)
        assert check_unique(combined_genotypes) is False
        
        