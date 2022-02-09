
import pytest
from .utils import split_and_clean_words

@pytest.mark.parametrize("sentence, expected_words", 
    [
        ["I love potatoes so much!", ["love", "potatoes", "much"]], 
        ["I love potatoes so much! us", ["love", "potatoes", "much"]],
        ["Potato-pickers are job-creating", ["potatopickers", "jobcreating"]], 
    ]
)
def test_split_and_clean_words(sentence, expected_words):
    """
    Given a simple sentence
    When split_and_clean_words
    Then I get a list of the cleaned words
    """
    result = split_and_clean_words(sentence)
    assert list(result.keys()) == expected_words