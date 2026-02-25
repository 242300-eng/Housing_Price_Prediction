import pytest
from app import normalize_value, SCALERS

def test_normalize_value_min():
    """Test if min value normalizes to 0"""
    feature = 'square'
    min_val = SCALERS[feature]['min']
    normalized = normalize_value(min_val, feature)
    assert normalized == 0

def test_normalize_value_max():
    """Test if max value normalizes to 1"""
    feature = 'followers'
    max_val = SCALERS[feature]['max']
    normalized = normalize_value(max_val, feature)
    assert normalized == 1

def test_normalize_value_mid():
    """Test a middle value"""
    feature = 'livingRoom' # min: 0, max: 8
    val = 4
    normalized = normalize_value(val, feature)
    assert normalized == 0.5

def test_invalid_feature():
    """Test if invalid feature returns original value"""
    val = 100
    assert normalize_value(val, 'non_existent_feature') == val
