from SSLP_App.utils import read_haplotypes,extract_sslps,generate_all_combinations
import pytest

def test_generate_all_combinations_empty_input_returns_empty_values():
    perm,total_perm = generate_all_combinations([],[],[])
    assert total_perm == 0
    assert isinstance(perm,list)
    assert len(perm) == 0
    
    
def test_generate_all_combinations_empty_selection_returns_empty_values():
    chr4,chr10 = extract_sslps([161,162,163,164],read_haplotypes("European"))
    perm,total_perm = generate_all_combinations([],chr4,chr10)
    assert total_perm == 0
    assert isinstance(perm,list)
    assert len(perm) == 0
    
def test_generate_all_combinations_empty_selection_returns_empty_values():
    chr4,chr10 = extract_sslps([161,162,163,164],read_haplotypes("European"))
    perm,total_perm = generate_all_combinations([],chr4,chr10)
    assert total_perm == 0
    assert isinstance(perm,list)
    assert len(perm) == 0
    
def test_generate_all_combinations_empty_chr_list_returns_empty_values():
    perm,total_perm = generate_all_combinations([161,162,163,164],[],[])
    assert total_perm == 0
    assert isinstance(perm,list)
    assert len(perm) == 0

def test_generate_all_combinations_valid_input_returns_valid_results():
    chr4,chr10 = extract_sslps([161,162,163,164],read_haplotypes("European"))
    perm,total_perm = generate_all_combinations([161,162,163,164],chr4,chr10)
    assert isinstance(total_perm,float)
    assert isinstance(perm,list)
    assert isinstance(perm[0],list)
    assert isinstance(perm[0][0],float)
    assert isinstance(perm[0][1],list)
    assert isinstance(perm[0][2],str)
    assert isinstance(perm[0][1][0],str)
    
