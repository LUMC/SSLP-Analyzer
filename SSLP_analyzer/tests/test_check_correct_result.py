from SSLP_App.utils import predict
import os
import pytest

# These tests are designed for the default dataset.


def test_predict_valid_input_European_result1():
    try:
        assert predict([161, 162, 163, 164], "European") == (
            [
                [0.004794451200000001, ["4B162", "4B163", "10B161T", "10A164"], 0],
                [0.004539673600000001, ["4A161", "4B163", "10A162", "10A164"], 1],
                [0.0001311552, ["4B162", "4A163", "10B161T", "10A164"], 1],
                [0.00012418560000000003, ["4A161", "4A163", "10A162", "10A164"], 2],
                [8.10656e-05, ["4B161", "4B163", "10A162", "10A164"], 0],
                [2.2176e-06, ["4A163", "4B161", "10A162", "10A164"], 0],
            ],
            0.009672748800000002,
        )
    except AssertionError:
        pytest.fail("Algorithm produced incorrect result")
    else:
        assert True


def test_predict_valid_input_European_result2():
    try:
        assert predict([161, 161, 161, 164], "European") == (
            [
                [0.06220318720000002, ["4A161", "4A161", "10B161T", "10A164"], 2],
                [0.0022215424, ["4A161", "4B161", "10A164", "10B161T"], 1],
                [1.9835199999999996e-05, ["4B161", "4B161", "10A164", "10B161T"], 1],
            ],
            0.06444456480000003,
        )
    except AssertionError:
        pytest.fail("Algorithm produced incorrect result")
    else:
        assert True


def test_predict_valid_input_European_no_result():
    try:
        assert predict([161, 174, 174, 174], "European") == (1, 1)
    except AssertionError:
        pytest.fail("Algorithm produced incorrect result")
    else:
        assert True


def test_predict_valid_input_Asian_result():
    try:
        assert predict([161, 163, 166, 170], "Asian") == (
            [
                [0.062263555199999994, ["4B170", "4B163", "10B161T", "10A166"], 0],
                [0.013630982399999998, ["4B170", "4B163", "10B161T", "10A166H"], 1],
                [0.0006519744000000001, ["4B170", "4A163", "10A166", "10B161T"], 1],
                [0.0001427328, ["4A163", "4B170", "10B161T", "10A166H"], 1],
            ],
            0.07668924479999999,
        )
    except AssertionError:
        pytest.fail("Algorithm produced incorrect result")
    else:
        assert True


def test_predict_valid_input_Asian_no_result():
    try:
        assert predict([161, 162, 163, 164], "Asian") == (1, 1)
    except AssertionError:
        pytest.fail("Algorithm produced incorrect result")
    else:
        assert True


def test_predict_valid_input_African_result():
    try:
        assert predict([157, 166, 166, 166], "African") == (
            [
                [0.392088, ["4A157", "4A166H", "10A166", "10A166"], 2],
                [0.2899817499999999, ["4A157", "4C166H", "10A166", "10A166"], 2],
                [0.067390125, ["4A157", "4A166", "10A166", "10A166"], 1],
                [0.03339071999999999, ["4A157", "4A166H", "10A166", "10A166H"], 3],
                [0.024695219999999997, ["4A157", "4C166H", "10A166H", "10A166"], 3],
                [0.016337, ["4A157", "4B166", "10A166", "10A166"], 1],
                [0.00573903, ["4A157", "4A166", "10A166", "10A166H"], 2],
                [0.0013912800000000002, ["4A157", "4B166", "10A166H", "10A166"], 2],
                [0.0007108991999999998, ["4A157", "4A166H", "10A166H", "10A166H"], 4],
                [0.0005257692, ["4A157", "4C166H", "10A166H", "10A166H"], 4],
                [0.0001221858, ["4A157", "4A166", "10A166H", "10A166H"], 3],
                [2.9620800000000003e-05, ["4B166", "4A157", "10A166H", "10A166H"], 3],
            ],
            0.8324015999999997,
        )
    except AssertionError:
        pytest.fail("Algorithm produced incorrect result")
    else:
        assert True


def test_predict_valid_input_African_no_result():
    try:
        assert predict([157, 159, 161, 163], "African") == (1, 1)
    except AssertionError:
        pytest.fail("Algorithm produced incorrect result")
    else:
        assert True
