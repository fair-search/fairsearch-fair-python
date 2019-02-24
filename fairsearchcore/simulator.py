# -*- coding: utf-8 -*-

"""
fairsearchcore.simulator
~~~~~~~~~~~~~~~
This module serves as a wrapper for simulator functionalities
"""

import random
from fairsearchcore import fair
from fairsearchcore import models


def generate_rankings(M, k:int, p):
    """
    Generates M rankings of n elements using Yang-Stoyanovich process
    :param M:           how many rankings to generate
    :param k:           how many elements should each ranking have
    :param p:           what is the probability that a candidate is protected
    :return:            the generated rankings (list of lists of FairScoreDoc))
    """
    rankings = []
    for m in range(M):
        rankings.append(_generate_ranking(k, p))

    return rankings


def compute_fail_probability(rankings, mtable):
    """
    This computes experimentally how many of the M rankings fail to satisfy the mtable
    :param rankings:    rankings that are checked (list of lists of FairScoreDoc)
    :param mtable:      an mtable to check against (list of int)
    :return:            the ratio of failed rankings
    """
    return len(list(filter(lambda x: not fair.check_ranking(x, mtable), rankings))) * 1.0 / len(rankings)


def _generate_ranking(k, p):
    """
    Create a ranking of 'k' positions in which at each position the
        probability that the candidate is protected is 'p'.
    """
    ranking = []
    for i in range(k):
        is_protected = (random.random() <= p)
        ranking.append(models.FairScoreDoc(k-i, k-i, is_protected))
    return ranking
