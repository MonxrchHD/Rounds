import pytest
from rounds.cleaning import find_abbreviations


def test_find_original_phrase():
    assert find_abbreviations("the presence of cotton-wool spots (CWS)") == {"CWS": "cotton-wool spots"}
    assert find_abbreviations("Non-proliferative diabetic retinopathy (NPDR)") == {"NPDR": "Non-proliferative diabetic retinopathy"}

def test_find_multiple_abbreviations():
    text = "cotton-wool spots (CWS) and non-proliferative diabetic retinopathy (NPDR)"
    result = find_abbreviations(text)
    assert result == {"CWS": "cotton-wool spots", "NPDR": "non-proliferative diabetic retinopathy"}

def test_find_start_capitalized_abbreviation():
    text = "Diabetic Retinopathy (DR) is the most frequent..."
    result = find_abbreviations(text)
    assert result == {"DR": "Diabetic Retinopathy"}

def test_find_no_abbreviation():
    text = "This text has no abbreviations."
    result = find_abbreviations(text)
    assert result == {}

def test_find_longer_abbreviation():
    text = "charaterized by intraretinal microvascular anomalies (IRMA)"
    result = find_abbreviations(text)
    assert result == {}

def test_find_abbreviation_at_start():
    text = "(OCT) images showed..."
    result = find_abbreviations(text)
    assert result == {}

def test_find_abbreviation_with_punctuation():
    text = "The patient had diabetic retinopathy, (DR) which was severe."
    result = find_abbreviations(text)
    assert result == {"DR": "diabetic retinopathy"}

def test_find_abbreviation_on_new_page():
    text = "The patient had diabetic\nretinopathy (DR) was diagnosed."
    result = find_abbreviations(text)
    assert result == {"DR": "diabetic retinopathy"}

def test_definition_followed_by_period():
    text = "The patient had diabetic retinopathy. (DR) was diagnosed."
    assert find_abbreviations(text) == {"DR": "diabetic retinopathy"}