from typing import List
import pyximport

importers = pyximport.install()
from cape_splitter.fast_tokenizer.word_tokenizer import word_tokenizer, sentence_tokenizer

pyximport.uninstall(*importers)
import pytest


def _spans_to_token_list(text: str, spans: List[List[int]]) -> List[str]:
    return [text[span[0]:span[1] + 1] for span in spans]


_TOKENIZED_WORDS = [
    ("  Hello World whaît a\nwonderful\tplace.!! ",
     ['  ', 'Hello ', 'World ', 'whaît ', 'a\n', 'wonderful\t', 'place.!! ']),
    ("This-is-a= two[word&sentence", ["This-is-a= ", "two[word&sentence"]),
    ("This-is-a@single.word", ["This-is-a@single.word"]),
    ("another/single/lonely.word", ["another/single/lonely.word"]),
    (("boundaries"), ["boundaries"]),
    ((" boundaries"), [" ", "boundaries"]),
    (("boundaries "), ["boundaries "]),
    (("\tboundaries\t"), ["\t", "boundaries\t"]),
    (("\nboundaries\n"), ["\n", "boundaries\n"]),
]

_TOKENIZED_SENTENCES = [
    ("  Hello World whaît a\nwonderful\tplace.!! ",
     ['  Hello World whaît a\nwonderful\tplace.!! ']),
    ("  Hello World whaît a\n wonderful\t place.!! ",
     ['  Hello World whaît a\n ', 'wonderful\t place.!! ']),
    (". How. many.sentences do? you! see?today? ",
     [". ", "How. ", "many.sentences do? ", "you! ", "see?today? "]),
    ("... Wait what is this ?!?For real?",
     ["... ", "Wait what is this ?!?For real?"]),
    ("Wait what is this ?!?For real?         ",
     ["Wait what is this ?!?For real?         "]),
    ("How many cows in the ranch,.,./\';][=--)(*(*&*^&^%^%$^%$##$@@!#$#± ?",
     ["How many cows in the ranch,.,./\';][=--)(*(*&*^&^%^%$^%$##$@@!#$#± ?"]),
    ("How many tigers in the jungle.....   \nI do not know,do you know ??? Nop!!!! ",
     ["How many tigers in the jungle.....   \n", "I do not know,do you know ??? ", "Nop!!!! "]),
]


@pytest.mark.parametrize("expectations", _TOKENIZED_WORDS)
def test_word_tokenizer(expectations):
    text, expected = expectations
    # assert we obtain the wanted tokens
    assert _spans_to_token_list(text, word_tokenizer(text)) == expected
    # assert we are doing lossless and reversible tokens
    assert text == "".join(expected)


@pytest.mark.parametrize("expectations", _TOKENIZED_SENTENCES)
def test_word_tokenizer(expectations):
    text, expected = expectations
    print(sentence_tokenizer(text))
    print(_spans_to_token_list(text, sentence_tokenizer(text)))
    # assert we obtain the wanted tokens
    assert _spans_to_token_list(text, sentence_tokenizer(text)) == expected
    # assert we are doing lossless and reversible tokens
    assert text == "".join(expected)
