from SSLP_App.utils import predict
import pytest

def test_predict_no_selection_returns_tuple_with_ints():
    population = "European"
    selection = [161,162,163,164]
    assert predict([],population) == (1,1)
    
def test_predict_no_population_raises_KeyError():
    population = "European"
    selection = [161,162,163,164]
    try:
        predict(selection,"")
    except Exception as e:
        assert isinstance(e,KeyError)
    else:
        pytest.fail("Exception not raised when expected")
        
def test_predict_valid_input_returns_valid_output():
    population = "European"
    selection = [161,162,163,164]
    try:
        percents,total_percents = predict(selection,population)
    except Exception as e:
        pytest.fail(f"Exception raised when not expected {e}")
    else:
        assert isinstance(total_percents,float)
        assert isinstance(percents,list)
        assert isinstance(percents[0],list)
        assert isinstance(percents[0][0],float)
        assert isinstance(percents[0][1],list)
        assert isinstance(percents[0][1][0],str)
        assert isinstance(percents[0][2],int)