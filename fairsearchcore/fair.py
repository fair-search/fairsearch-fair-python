# -*- coding: utf-8 -*-

"""
This module serves as a wrapper around the utilities we have created for FA*IR ranking
"""
import pandas as pd
import warnings

from fairsearchcore import mtable_generator
from fairsearchcore import fail_prob


class Fair:

    k = 10  # the total number of elements
    p = 0.2  # the proportion of protected candidates in the top-k ranking
    alpha = 0.1  # the significance level

    def __init__(self, k: int, p: float, alpha: float):
        # check the parameters first
        _validate_basic_parameters(k, p, alpha)

        # assign the parameters
        self.k = k
        self.p = p
        self.alpha = alpha

    def create_unadjusted_mtable(self) -> list:
        """
        Creates an mtable using alpha unadjusted
        :return:
        """
        return self._create_mtable(self.alpha, False)

    def create_adjusted_mtable(self) -> list:
        """
        Creates an mtable using alpha adjusted
        :return:
        """
        return self._create_mtable(self.alpha, True)

    def _create_mtable(self, alpha: int, adjust_alpha: bool) -> list:
        """
        Creates an mtable by using the passed alpha value
        :param alpha:           The significance level
        :param adjust_alpha:    Boolean indicating whether the alpha be adjusted or not
        :return:
        """
        # check if passed alpha is ok
        _validate_alpha(alpha)

        # create the mtable
        fc = mtable_generator.MTableGenerator(self.k, self.p, alpha, adjust_alpha)

        # return as list
        return fc.mtable_as_list()

    def adjust_alpha(self):
        """
        Computes the alpha adjusted for the given set of parameters
        :return:
        """
        rnfpc = fail_prob.RecursiveNumericFailprobabilityCalculator(self.k, self.p, self.alpha)
        fpp = rnfpc.adjust_alpha()
        return fpp.alpha

    def compute_fail_probability(self, mtable):
        """
        Computes analytically the probability that a ranking created with the simulator will fail to pass the mtable
        :return:
        """
        if len(mtable) != self.k:
            raise ValueError("Number of elements k and mtable length must be equal!")

        rnfpc = fail_prob.RecursiveNumericFailprobabilityCalculator(self.k, self.p, self.alpha)

        mtable_df = pd.DataFrame(columns=["m"])

        # transform the list into an pd.DataFrame
        for i in range(1, len(mtable) + 1):
            mtable_df.loc[i] = [mtable[i-1]]

        return rnfpc.calculate_fail_probability(mtable_df)

    def is_fair(self, ranking: list) -> bool:
        """
        Checks if the ranking is fair for the given parameters
        :param ranking:     The ranking to be checked
        :return:
        """
        return check_ranking(ranking, self.create_adjusted_mtable())


def check_ranking(ranking:list, mtable: list) -> bool:
    """
    Checks if the ranking is fair in respect to the mtable
    :param ranking:     The ranking to be checked
    :param mtable:      The mtable against to check
    :return:            Returns whether the rankings statisfies the mtable
    """
    count_protected = 0

    # if the mtable has a different number elements than there are in the top docs return false
    if len(ranking) != len(mtable):
        raise ValueError("Number of documents in ranking and mtable length must be equal!")

    # check number of protected element at each rank
    for i, element in enumerate(ranking):
        count_protected += 1 if element == 1 else 0
        if count_protected < mtable[i]:
            return False
    return True


def _validate_basic_parameters(k: int, p: float, alpha: float):
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


def _validate_alpha(alpha: float):
    if alpha < 0.01 or alpha > 0.15:
        if alpha < 0.001 or alpha > 0.5:
            raise ValueError("The significance level `alpha` must be between 0.01 and 0.15")
        else:
            warnings.warn("Library has not been tested with values outside this range")

