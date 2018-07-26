from typing import Tuple
from collections import OrderedDict
from cape_splitter.fast_tokenizer.word_tokenizer import word_tokenizer, sentence_tokenizer

def get_n_words_before_position(str doc, sentences, int offset, int number_of_words)-> str:
    cdef int end_span
    cdef int current_words
    cdef int remaining_words
    cdef int beg_span
    cdef int size_sentence
    if offset == 0:
        return ""
    end_span = sentences[offset][0][0]
    current_words = 0
    beg_span = -1
    while offset > 0:
        offset -= 1
        remaining_words = number_of_words - current_words
        size_sentence = len(sentences[offset])
        if size_sentence >= remaining_words:
            break
        else:
            current_words += size_sentence
    else:
        beg_span = sentences[offset][0][0]
    if beg_span == -1:
        beg_span = sentences[offset][-remaining_words][0]
    return doc[beg_span:end_span]

def get_n_words_after_position(str doc, sentences, int offset, int number_of_words)-> str:
    cdef int end_span
    cdef int current_words
    cdef int remaining_words
    cdef int beg_span
    cdef int size_sentence
    max_offset = len(sentences) - 1
    beg_span = sentences[offset][0][0]
    current_words = 0
    end_span = -1
    while offset <= max_offset:
        remaining_words = number_of_words - current_words
        size_sentence = len(sentences[offset])
        if size_sentence >= remaining_words:
            break
        else:
            current_words += size_sentence
        offset += 1
    else:
        end_span = sentences[offset - 1][-1][1] + 1
    if end_span == -1:
        end_span = sentences[offset][remaining_words - 1][1] + 1
    return doc[beg_span:end_span]


class TextGroup:
    idx: int
    parent_doc_id: str
    number_of_words: int
    text: str
    text_span: Tuple[int, int]
    overlap_before: str
    overlap_after: str


def make_group(str doc, sentences, groups_sizes, groups_offsets, int idx, str doc_id, int words_before,
               int words_after):
    text_group = TextGroup()
    text_group.idx = idx
    text_group.parent_doc_id = doc_id
    offset = groups_offsets[idx]
    try:
        next_offset = groups_offsets[idx + 1]
        end_span = sentences[next_offset][0][0]
        text_group.overlap_after = get_n_words_after_position(doc, sentences, next_offset, words_after)
    except IndexError:
        end_span = sentences[-1][-1][-1] + 1
        text_group.overlap_after = ""
    text_group.text_span = [sentences[offset][0][0], end_span]
    text_group.text = doc[text_group.text_span[0]:text_group.text_span[1]]
    text_group.overlap_before = get_n_words_before_position(doc, sentences, offset, words_before)
    text_group.number_of_words = groups_sizes[idx]
    return text_group

def make_groups(document_ids, document_texts,int words_per_group,int max_overlap_before,int max_overlap_after):
    total_number_words = 0
    document_groups = OrderedDict()
    for doc_id, doc in zip(document_ids, document_texts):
        sentences = []
        for sentence_span in sentence_tokenizer(doc):
            sentences.append(word_tokenizer(doc[sentence_span[0]:sentence_span[1] + 1], sentence_span[0]))
        current_words = words_per_group
        groups_offsets = []
        groups_sizes = []
        for idx, spans in enumerate(sentences):
            len_spans = len(spans)
            if current_words + len_spans < words_per_group:  # Existing group
                current_words += len_spans
                groups_sizes[-1] = current_words
            else:
                groups_offsets.append(idx)
                current_words = len_spans
                groups_sizes.append(current_words)
            total_number_words += len_spans
        document_groups[doc_id] = [
            make_group(doc, sentences, groups_sizes, groups_offsets, idx, doc_id, max_overlap_before,
                       max_overlap_after)
            for idx in range(len(groups_offsets))]
    return document_groups, total_number_words
