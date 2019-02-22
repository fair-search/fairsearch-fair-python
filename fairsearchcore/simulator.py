# -*- coding: utf-8 -*-

"""
This module serves as a wrapper for simulator functionalities
"""

import random
from fairsearchcore import fair


def generate_rankings(M, k, p):
    """
    Generates M rankings of n elements using Yang-Stoyanovich process
    :param M:           how many rankings to generate
    :param k:           how many elements should each ranking have
    :param p:           what is the probability that a candidate is protected
    :return:            the generated rankings (list of lists)
    """
    rankings = []
    for m in range(M):
        rankings.append(_generate_ranking(k, p))

    return rankings


def compute_fail_probabilty(rankings, mtable):
    """
    This computes experimentally how many of the M rankings fail to satisfy the mtable
    :param rankings:    rankings that are checked
    :param mtable:      an mtable to check against
    :return:            the ratio of failed rankings
    """
    return len(list(filter(lambda x: not fair.check_ranking(x, mtable), rankings))) * 1.0 / len(rankings)


def _generate_ranking(k, p):
    ''' Create a ranking of 'k' positions in which at each position the
        probability that the candidate is protected is 'p'.
    '''
    ranking = []
    for i in range(k):
        is_protected = (random.random() <= p)
        if is_protected:
            ranking.append(1)
        else:
            ranking.append(0)
    return ranking