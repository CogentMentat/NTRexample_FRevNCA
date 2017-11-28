# coding: utf-8
"""
Example code for producing topic mixtures, given a file of text data.

Author: Alexander T. J. Barron
Date Created: 2017-11-25

"""

import argparse
import os

import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from lda import LDA

def learn_topics(textpath, topicnum):

    with open(textpath) as f:
        texts = f.readlines()

    # Get vocabulary and word counts.  Use the top 10,000 most frequent
    # lowercase unigrams with at least 3 alphabetical, non-numeric characters,
    # punctuation treated as separators.
    CVzer = CountVectorizer(token_pattern=r"(?u)\b[^\W\d]{3,}\b",
                            max_features=None,
                            lowercase=True)
    doc_vcnts = CVzer.fit_transform(texts)
    vocabulary = CVzer.get_feature_names()

    # Learn topics.  Refresh conrols print frequency.
    lda_model = LDA(topicnum, n_iter=8000, refresh=2000) 
    doc_topic = lda_model.fit_transform(doc_vcnts)
    topic_word = lda_model.topic_word_

    return doc_topic, topic_word, vocabulary

def save_topicmodel(doc_topic, topic_word, vocabulary, dirpath):

    ## Topic mixtures.
    topicmixture_outpath = os.path.join(dirpath, "topic_mixtures.txt")
    np.savetxt(topicmixture_outpath, doc_topic)

    ## Topics.
    topic_outpath = os.path.join(dirpath, "topics.txt")
    np.savetxt(topic_outpath, topic_word)

    ## Vocabulary order.
    vocab_outpath = os.path.join(dirpath, "vocabulary.txt")
    with open(vocab_outpath, mode="w") as f:
        for v in vocabulary:
            f.write(v + "\n")

    return topicmixture_outpath, topic_outpath, vocab_outpath

def main(textpath, topicnum, dirpath):

    doc_topic, topic_word, vocabulary = learn_topics(textpath, topicnum)

    topicmixture_outpath, topic_outpath, vocab_outpath = \
            save_topicmodel(doc_topic, topic_word, vocabulary, dirpath)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("textpath", type=str,
           help="Path to file of text data, one document per row, " \
                   "rows delimited with newlines.") 
    parser.add_argument("topicnum", type=int,
            help="Desired number of topics.")
    parser.add_argument("dirpath", type=str,
           help="Directory path to enclose results.") 
    args = parser.parse_args()

    main(args.textpath, args.topicnum, args.dirpath)
