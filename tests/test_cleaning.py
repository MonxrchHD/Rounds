
from rounds.cleaning import find_abbreviations, expand_abbreviations

ABBREVIATIONS = {
    "CWS": "cotton-wool spots",
    "ON": "optic nerve",
    "DR": "diabetic retinopathy",
    "NPDR": "non-proliferative diabetic retinopathy",
}


def test_expands_abbreviation_keeping_both_forms():
    text = "the so-called CWS were present"
    assert expand_abbreviations(text, ABBREVIATIONS) == (
        "the so-called CWS (cotton-wool spots) were present"
    )


def test_does_not_touch_lowercase_word():
    text = "spots on the retina"
    assert expand_abbreviations(text, ABBREVIATIONS) == text


def test_does_not_expand_inside_longer_word():
    text = "ONH cupping"
    assert expand_abbreviations(text, ABBREVIATIONS) == text


def test_expands_overlapping_abbreviations_correctly():
    text = "NPDR is a stage of DR"
    assert expand_abbreviations(text, ABBREVIATIONS) == (
        "NPDR (non-proliferative diabetic retinopathy) is a stage of "
        "DR (diabetic retinopathy)"
    )


def test_expands_next_to_punctuation():
    text = "Findings: CWS, DR."
    assert expand_abbreviations(text, ABBREVIATIONS) == (
        "Findings: CWS (cotton-wool spots), DR (diabetic retinopathy)."
    )


def test_empty_dictionary_returns_text_unchanged():
    text = "the so-called CWS were present"
    assert expand_abbreviations(text, {}) == text
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