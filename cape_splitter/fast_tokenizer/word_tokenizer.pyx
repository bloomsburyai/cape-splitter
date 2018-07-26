
import re

NON_WORD_CHARS = re.compile('[\s]+|\Z')
END_SENTENCE_CHARS = re.compile('[%s]+\s+|\Z' % re.escape(''.join(['.', '?', '!', ';', '\n', '\r'])))

def word_tokenizer(str text, int offset=0):
    return tokenizer(text, NON_WORD_CHARS, offset)

def sentence_tokenizer(str text, int offset=0):
    return tokenizer(text, END_SENTENCE_CHARS, offset)

def tokenizer(str text, object pattern, int offset):
    cdef int previous
    previous = offset
    spans = []
    for match in re.finditer(pattern, text):
        end = offset + match.end(0)
        if end>previous:
            spans.append((previous, end - 1))
        previous = end
    if spans:
        return spans
    else:
        return [[offset,len(text)]]

# This tokenizer was actually slower due to str to bytes conversions
# from libc.string cimport strlen, strpbrk
# from libcpp.vector cimport vector
# def word_tokenizer(str text):
#     """Return the offsets"""
#     # Encoding allows us to simplify the tokenization and to work in C :
#     # print("@ Déjà, quel gâteau\n êtes-vous ?".encode('ascii','replace')) ->'@ D?j?, quel g?teau\n ?tes-vous ?'
#     return _word_tokenizer(text.encode('ascii','replace'))
#
# cdef vector[vector[int]] _word_tokenizer(char* text):
#     cdef int length
#     cdef char* textcopy
#     cdef size_t separator
#     cdef vector[vector[int]] vect
#     cdef int position
#     cdef int previous
#     separator=1
#     textcopy = text
#     length = strlen(text)
#     previous = 0
#     while True:
#         textcopy = strpbrk(textcopy, ' ')
#         if textcopy:
#             position = textcopy-text
#             if previous != position:
#                 vect.push_back((previous,position))
#             if position+1 == length:
#                 break
#             textcopy += separator
#             previous = position+1
#         else:
#             break
#     return vect
