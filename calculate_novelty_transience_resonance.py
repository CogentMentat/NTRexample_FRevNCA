# coding: utf-8
"""
Example code for calculating novelty, transience, and resonance.

Author: Alexander T. J. Barron
Date Created: 2017-11-09

"""

import os
import argparse

import numpy as np

def KLdivergence_from_probdist_arrays(pdists0, pdists1):
    """
    Calculate KL divergence between probability distributions held on the same
    rows of two arrays.

    NOTE: elements of pdist* are assumed to be positive (non-zero), a
    necessary condition for using Kullback-Leibler Divergence.

    Args:
      pdists* (numpy.ndarray): arrays, where rows for each constitute the two
      probability distributions from which to calculate divergence.  pdists1
      contains the distributions holding probabilities in the numerator of the
      KL divergence summand.

    Returns:
      numpy.ndarray: KL divergences, where the second array's rows are the
        distributions in the numerator of the log in KL divergence

    """

    assert pdists0.shape == pdists1.shape, 'pdist* shapes must be identical'

    if len(pdists0.shape) == 1:
        KLdivs = (pdists1 * np.log2(pdists1/pdists0)).sum()
    elif len(pdists0.shape) == 2:
        KLdivs = (pdists1 * np.log2(pdists1/pdists0)).sum(axis=1)

    return KLdivs

def novelty_transience_resonance(thetas_arr, scale):
    """
    Calculate novelty, transience, and resonance for all center speeches with
    at least one scale of speeches in its past and its future.  Presidential
    speeches are excluded from the surrounding scales.
    
    Args:
      thetas_arr (numpy.ndarray): rows are topic mixtures
      scale (int): positive integer defining scale or scale size
    
    """

    # Find the first and last center speech offset, given scale size.
    speechstart = scale
    speechend = thetas_arr.shape[0] - scale

    # Calculate novelty, transience, resonance.
    novelties = []
    transiences = []
    resonances = []
    for j in range(speechstart, speechend, 1):

        center_theta = thetas_arr[j]

        # Define windows before and after center speech.
        after_boxend = j + scale + 1
        before_boxstart = j - scale

        before_theta_arr = thetas_arr[before_boxstart:j]
        beforenum = before_theta_arr.shape[0]
        before_centertheta_arr = np.tile(center_theta, reps=(beforenum, 1))

        after_theta_arr = thetas_arr[j+1:after_boxend]
        afternum = after_theta_arr.shape[0]
        after_centertheta_arr = np.tile(center_theta, reps=(afternum, 1))

        # Calculate KLDs.
        before_KLDs = KLdivergence_from_probdist_arrays(before_theta_arr,
                before_centertheta_arr)
        after_KLDs = KLdivergence_from_probdist_arrays(after_theta_arr,
                after_centertheta_arr)

        # Calculate means of KLD.
        novelty = np.mean(before_KLDs)
        transience = np.mean(after_KLDs)

        # Final measures for this center speech.
        novelties.append(novelty)
        transiences.append(transience)
        resonances.append(novelty - transience)

    return novelties, transiences, resonances

def save_novel_trans_reson(novelties, transiences, resonances, dirpath):

    outpath = os.path.join(dirpath, "novel_trans_reson.txt")
    np.savetxt(outpath, np.vstack(zip(novelties, transiences, resonances)))

def main(topic_mixture_path, scale, dirpath):

    thetas_arr = np.loadtxt(topic_mixture_path)

    novelties, transiences, resonances = \
            novelty_transience_resonance(thetas_arr, scale)

    save_novel_trans_reson(novelties, transiences, resonances, dirpath)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("topic_mixture_path", type=str,
           help="Path to text file of topic mixtures, one per row, " \
                   "elements delimited with whitespace, " \
                   "rows delimited with newlines.") 
    parser.add_argument("scale", type=int,
            help="Size of windows for calculation.")
    parser.add_argument("dirpath", type=str,
           help="Directory path to enclose results.") 
    args = parser.parse_args()

    main(args.topic_mixture_path, args.scale, args.dirpath)
