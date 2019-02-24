# -*- coding: utf-8 -*-

"""
fairsearchcore.fair
~~~~~~~~~~~~~~~
This module serves as a wrapper around the utilities we have created for FA*IR ranking
"""

import pandas as pd
import warnings

from fairsearchcore import mtable_generator
from fairsearchcore import fail_prob
from fairsearchcore import re_ranker


class Fair:
    def __init__(self, k: int, p: float, alpha: float):
        # check the parameters first
        _validate_basic_parameters(k, p, alpha)

        # assign the parameters
        self.k = k # the total number of elements
        self.p = p # the proportion of protected candidates in the top-k ranking
        self.alpha = alpha # the significance level

        self. _cache = {}  # stores generated mtables in memory

    def create_unadjusted_mtable(self):
        """
        Creates an mtable using alpha unadjusted
        :return:
        """
        return self._create_mtable(self.alpha, False)

    def create_adjusted_mtable(self):
        """
        Creates an mtable using alpha adjusted
        :return:
        """
        return self._create_mtable(self.alpha, True)

    def _create_mtable(self, alpha, adjust_alpha):
        """
        Creates an mtable by using the passed alpha value
        :param alpha:           The significance level
        :param adjust_alpha:    Boolean indicating whether the alpha be adjusted or not
        :return:
        """

        if not (self.k, self.p, self.alpha, adjust_alpha) in self._cache:
            # check if passed alpha is ok
            _validate_alpha(alpha)

            # create the mtable
            fc = mtable_generator.MTableGenerator(self.k, self.p, alpha, adjust_alpha)

            # store as list
            self._cache[(self.k, self.p, self.alpha, adjust_alpha)] = fc.mtable_as_list()

        # return from cache
        return self._cache[(self.k, self.p, self.alpha, adjust_alpha)]

    def adjust_alpha(self) :
        """
        Computes the alpha adjusted for the given set of parameters
        :return:
        """
        rnfpc = fail_prob.RecursiveNumericFailProbabilityCalculator(self.k, self.p, self.alpha)
        fpp = rnfpc.adjust_alpha()
        return fpp.alpha

    def compute_fail_probability(self, mtable):
        """
        Computes analytically the probability that a ranking created with the simulator will fail to pass the mtable
        :return:
        """
        if len(mtable) != self.k:
            raise ValueError("Number of elements k and mtable length must be equal!")

        rnfpc = fail_prob.RecursiveNumericFailProbabilityCalculator(self.k, self.p, self.alpha)

        mtable_df = pd.DataFrame(columns=["m"])

        # transform the list into an pd.DataFrame
        for i in range(1, len(mtable) + 1):
            mtable_df.loc[i] = [mtable[i-1]]

        return rnfpc.calculate_fail_probability(mtable_df)

    def is_fair(self, ranking):
        """
        Checks if the ranking is fair for the given parameters
        :param ranking:     The ranking to be checked (list of FairScoreDoc)
        :return:
        """
        return check_ranking(ranking, self.create_adjusted_mtable())

    def re_rank(self, ranking):
        """
        Applies FA*IR re-ranking to the input ranking with an adjusted mtable
        :param ranking:     The ranking to be re-ranked (list of FairScoreDoc)
        :return:
        """
        return self._re_rank(ranking, True)

    def _re_rank_unadjusted(self, ranking):
        """
        Applies FA*IR re-ranking to the input ranking with an unadjusted mtable
        :param ranking:     The ranking to be re-ranked (list of FairScoreDoc)
        :return:
        """
        return self._re_rank(ranking, False)

    def _re_rank(self, ranking, adjust):
        """
        Applies FA*IR re-ranking to the input ranking and boolean whether to use an adjusted mtable
        :param ranking:     The ranking to be re-ranked (list of FairScoreDoc)
        :return:
        """
        protected = []
        non_protected = []
        for item in ranking:
            if item.is_protected:
                protected.append(item)
            else:
                non_protected.append(item)

        return re_ranker.fair_top_k(self.k, protected, non_protected,
                                    self.create_adjusted_mtable() if adjust else self.create_unadjusted_mtable())


def check_ranking(ranking, mtable):
    """
    Checks if the ranking is fair in respect to the mtable
    :param ranking:     The ranking to be checked (list of FairScoreDoc)
    :param mtable:      The mtable against to check (list of int)
    :return:            Returns whether the rankings satisfies the mtable
    """
    count_protected = 0

    # if the mtable has a different number elements than there are in the top docs return false
    if len(ranking) != len(mtable):
        raise ValueError("Number of documents in ranking and mtable length must be equal!")

    # check number of protected element at each rank
    for i, element in enumerate(ranking):
        count_protected += 1 if element.is_protected else 0
        if count_protected < mtable[i]:
            return False
    return True


def _validate_basic_parameters(k, p, alpha):
    """
    Validates if k, p and alpha are in the required ranges
    :param k:           Total number of elements (above or equal to 10)
    :param p:           The proportion of protected candidates in the top-k ranking (between 0.02 and 0.98)
    :param alpha:       The significance level (between 0.01 and 0.15)
    """
    if k < 10 or k > 400:
        if k < 2:
            raise ValueError("Total number of elements `k` should be between 10 and 400")
        else:
            warnings.warn("Library has not been tested with values outside this range")

    if p < 0.02 or p > 0.98:
        if p < 0 or p > 1:
            raise ValueError("The proportion of protected candidates `p` in the top-k ranking should be between "
                             "0.02 and 0.98")
        else:
            warnings.warn("Library has not been tested with values outside this range")

    _validate_alpha(alpha)


def _validate_alpha(alpha):
    if alpha < 0.01 or alpha > 0.15:
        if alpha < 0.001 or alpha > 0.5:
            raise ValueError("The significance level `alpha` must be between 0.01 and 0.15")
        else:
            warnings.warn("Library has not been tested with values outside this range")

