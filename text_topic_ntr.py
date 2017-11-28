# coding: utf-8
"""
Script executing topic modeling and calculation of novelty, transience, and
resonance in succession.

Author: Alexander T. J. Barron
Date Created: 2017-11-25

"""

import argparse

from learn_topics import learn_topics, save_topicmodel
from calculate_novelty_transience_resonance import \
        novelty_transience_resonance, save_novel_trans_reson

def main(textpath, topicnum, scale, dirpath):

    doc_topic, topic_word, vocabulary = learn_topics(textpath, topicnum)

    topicmixture_outpath, topic_outpath, vocab_outpath = \
            save_topicmodel(doc_topic, topic_word, vocabulary, dirpath)

    novelties, transiences, resonances = \
            novelty_transience_resonance(doc_topic, scale)

    save_novel_trans_reson(novelties, transiences, resonances, dirpath)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("textpath", type=str,
           help="Path to file of text data, one document per row, " \
                   "rows delimited with newlines.") 
    parser.add_argument("topicnum", type=int,
            help="Desired number of topics.")
    parser.add_argument("scale", type=int,
            help="Size of windows for calculation.")
    parser.add_argument("dirpath", type=str,
           help="Directory path to enclose results.") 
    args = parser.parse_args()

    main(args.textpath, args.topicnum, args.scale, args.dirpath)
