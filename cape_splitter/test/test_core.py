from cape_splitter.splitter_core import Splitter, word_tokenizer, sentence_tokenizer
import pytest
import datetime


def test_main():
    document_texts = [
        'The Normans (Norman: Nourmands; French: Normands; Latin: Normanni) were the people who in '
        'the 10th and 11th centuries gave their name to Normandy, a region in France. They were '
        'descended from Norse ("Norman" comes from "Norseman") raiders and pirates from Denmark, '
        'Iceland and Norway who, under their leader Rollo, agreed to swear fealty to King Charles '
        'III of West Francia. Through generations of assimilation and mixing with the native '
        'Frankish and Roman-Gaulish populations, their descendants would gradually merge with the '
        'Carolingian-based cultures of West Francia. The distinct cultural and ethnic identity of '
        'the Normans emerged initially in the first half of the 10th century, and it continued to '
        'evolve over the succeeding centuries.',
        'This is another irrelevant document',
        'This is the third document. It is also highly irrelevant.'
    ]
    document_ids = list(map(str, range(len(document_texts))))
    spl = Splitter(document_ids, document_texts, words_per_group=50)
    # for doc in spl.group_collection.document_groups:
    #     print("DOC", doc)
    #     for group in spl.group_collection.document_groups[doc]:
    #         print(group.__dict__)
    assert spl.document_groups['0'][0].__dict__ == {'idx': 0, 'parent_doc_id': '0',
                                                    'text_span': [0, 167],
                                                    'text': 'The Normans (Norman: Nourmands; French: Normands; Latin: Normanni) were the people who in the 10th and 11th centuries gave their name to Normandy, a region in France. ',
                                                    'overlap_before': '',
                                                    'overlap_after': 'They were descended from Norse ("Norman" comes from "Norseman") raiders and pirates from Denmark, Iceland and Norway who, under their leader Rollo, agreed to swear fealty to King Charles III of West Francia. Through generations of assimilation and mixing with the native Frankish and Roman-Gaulish populations, their descendants would gradually ',
                                                    'number_of_words': 27}
    assert spl.document_groups['0'][1].__dict__ == {'idx': 1, 'parent_doc_id': '0',
                                                    'text_span': [167, 375],
                                                    'text': 'They were descended from Norse ("Norman" comes from "Norseman") raiders and pirates from Denmark, Iceland and Norway who, under their leader Rollo, agreed to swear fealty to King Charles III of West Francia. ',
                                                    'overlap_before': 'The Normans (Norman: Nourmands; French: Normands; Latin: Normanni) were the people who in the 10th and 11th centuries gave their name to Normandy, a region in France. ',
                                                    'overlap_after': 'Through generations of assimilation and mixing with the native Frankish and Roman-Gaulish populations, their descendants would gradually merge with the Carolingian-based cultures of West Francia. The distinct cultural and ethnic identity of the Normans emerged initially in the first half of the 10th century, and it continued to evolve over ',
                                                    'number_of_words': 33}
    assert spl.document_groups['0'][2].__dict__ == {'idx': 2, 'parent_doc_id': '0',
                                                    'text_span': [375, 571],
                                                    'text': 'Through generations of assimilation and mixing with the native Frankish and Roman-Gaulish populations, their descendants would gradually merge with the Carolingian-based cultures of West Francia. ',
                                                    'overlap_before': 'people who in the 10th and 11th centuries gave their name to Normandy, a region in France. They were descended from Norse ("Norman" comes from "Norseman") raiders and pirates from Denmark, Iceland and Norway who, under their leader Rollo, agreed to swear fealty to King Charles III of West Francia. ',
                                                    'overlap_after': 'The distinct cultural and ethnic identity of the Normans emerged initially in the first half of the 10th century, and it continued to evolve over the succeeding centuries.',
                                                    'number_of_words': 25}
    assert spl.document_groups['0'][3].__dict__ == {'idx': 3, 'parent_doc_id': '0',
                                                    'text_span': [571, 742],
                                                    'text': 'The distinct cultural and ethnic identity of the Normans emerged initially in the first half of the 10th century, and it continued to evolve over the succeeding centuries.',
                                                    'overlap_before': '"Norseman") raiders and pirates from Denmark, Iceland and Norway who, under their leader Rollo, agreed to swear fealty to King Charles III of West Francia. Through generations of assimilation and mixing with the native Frankish and Roman-Gaulish populations, their descendants would gradually merge with the Carolingian-based cultures of West Francia. ',
                                                    'overlap_after': '', 'number_of_words': 28}
    assert spl.document_groups['1'][0].__dict__ == {'idx': 0, 'parent_doc_id': '1',
                                                    'text_span': [0, 35],
                                                    'text': 'This is another irrelevant document',
                                                    'overlap_before': '', 'overlap_after': '',
                                                    'number_of_words': 5}
    assert spl.document_groups['2'][0].__dict__ == {'idx': 0, 'parent_doc_id': '2',
                                                    'text_span': [0, 57],
                                                    'text': 'This is the third document. It is also highly irrelevant.',
                                                    'overlap_before': '', 'overlap_after': '',
                                                    'number_of_words': 10}
    assert spl.total_number_words == sum(
        len(word_tokenizer(text[span[0]:span[1] + 1])) for text in document_texts for span in sentence_tokenizer(text))


# TODO actually use this
def test_chunks():
    document_texts = [
        'The Normans (Norman: Nourmands; French: Normands; Latin: Normanni) were the people who in '
        'the 10th and 11th centuries gave their name to Normandy, a region in France. They were '
        'descended from Norse ("Norman" comes from "Norseman") raiders and pirates from Denmark, '
        'Iceland and Norway who, under their leader Rollo, agreed to swear fealty to King Charles '
        'III of West Francia. Through generations of assimilation and mixing with the native '
        'Frankish and Roman-Gaulish populations, their descendants would gradually merge with the '
        'Carolingian-based cultures of West Francia. The distinct cultural and ethnic identity of '
        'the Normans emerged initially in the first half of the 10th century, and it continued to '
        'evolve over the succeeding centuries.',
        'This is another irrelevant document',
        'This is the third document. It is also highly irrelevant.'
    ]
    document_ids = list(map(str, range(len(document_texts))))
    splitter = Splitter(document_ids, document_texts, words_per_group=50)
    for doc in splitter.document_groups:
        print("DOC", doc)
        for group in splitter.document_groups[doc]:
            print(group.__dict__)
    assert splitter.total_number_words == 128
    assert splitter.get_chunks(3) == [[('0', 0)], [('0', 1)], [('0', 2)], [('0', 3), ('1', 0)], [('2', 0)]]
    assert splitter.get_chunks(2) == [[('0', 0), ('0', 1)], [('0', 2), ('0', 3), ('1', 0)], [('2', 0)]]
    assert splitter.get_chunks(1) == [[('0', 0), ('0', 1), ('0', 2), ('0', 3), ('1', 0), ('2', 0)]]
    assert "".join(splitter.document_groups[doc_id][group_idx].text
                   for chunks in splitter.get_chunks(3)
                   for (doc_id, group_idx) in chunks) == "".join(document_texts)
    assert "".join(splitter.document_groups[doc_id][group_idx].text
                   for chunks in splitter.get_chunks(2)
                   for (doc_id, group_idx) in chunks) == "".join(document_texts)
    assert "".join(splitter.document_groups[doc_id][group_idx].text
                   for chunks in splitter.get_chunks(1)
                   for (doc_id, group_idx) in chunks) == "".join(document_texts)
