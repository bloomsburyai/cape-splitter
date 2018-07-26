from typing import List, Tuple, Dict, Any, Optional
import time
import pyximport
from collections import OrderedDict
from dataclasses import dataclass

importers = pyximport.install()

from cape_splitter.fast_tokenizer.word_tokenizer import word_tokenizer, sentence_tokenizer
from cape_splitter.fast_grouper.grouper_core import make_groups, TextGroup

pyximport.uninstall(*importers)


@dataclass
class Splitter:
    """
    Split the documents into groups, keeping full sentences.
    """
    document_ids: List[str]
    document_texts: List[str]
    total_number_words: int = None
    document_groups: OrderedDict = None  # like Dict[str, List[TextGroup]]
    words_per_group: int = 500
    max_overlap_before: int = 50
    max_overlap_after: int = 50

    def __post_init__(self):
        assert len(self.document_ids) == len(self.document_texts), "All documents must have an id"
        self.document_groups, self.total_number_words = make_groups(self.document_ids, self.document_texts,
                                                                    self.words_per_group,
                                                                    self.max_overlap_before, self.max_overlap_after)

    def get_chunks(self, number_of_chunks) -> List[List[Tuple[str, int]]]:
        """Get N chunks of groups"""
        chunks = []
        ideal_words_per_chunk = self.total_number_words // number_of_chunks
        current_words = ideal_words_per_chunk
        for doc_id, text_groups in self.document_groups.items():
            for text_group in text_groups:
                if current_words + text_group.number_of_words <= ideal_words_per_chunk:
                    chunks[-1].append((text_group.parent_doc_id, text_group.idx))
                    current_words += text_group.number_of_words
                else:
                    chunks.append([(text_group.parent_doc_id, text_group.idx)])
                    current_words = text_group.number_of_words
        return chunks


if __name__ == '__main__':
    from datasets import squad


    def pdict(adict):
        print('-' * 30)
        for key, val in adict.items():
            print(key, ':', repr(val))
        print('-' * 30)


    tic = time.time()
    spl = Splitter(list(map(str, range(len(squad.get_documents())))), squad.get_documents())
    print("tokenized all in ", time.time() - tic, "secs")
    pdict(spl.document_groups["0"][0].__dict__)

    pdict(spl.document_groups["9"][0].__dict__)
    pdict(spl.document_groups["9"][1].__dict__)
    print("total words", spl.total_number_words)
    print("total docs", len(squad.get_documents()))
    print("total groups", len(spl.document_groups.keys()))
