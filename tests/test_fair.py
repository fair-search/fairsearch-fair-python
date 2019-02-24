import pytest

from fairsearchcore import fair
from fairsearchcore import models

@pytest.mark.parametrize("k, p, alpha, ranking",(
                         (20, 0.25, 0.1, [models.FairScoreDoc(20,20,False),models.FairScoreDoc(19,19,True),
                                          models.FairScoreDoc(18,18,False),models.FairScoreDoc(17,17,False),
                                          models.FairScoreDoc(16,16,False),models.FairScoreDoc(15,15,False),
                                          models.FairScoreDoc(14,14,False),models.FairScoreDoc(13,13,True),
                                          models.FairScoreDoc(12,12,False),models.FairScoreDoc(11,11,True),
                                          models.FairScoreDoc(10,10,False),models.FairScoreDoc(9,9,False),
                                          models.FairScoreDoc(8,8,True),models.FairScoreDoc(7,7,False),
                                          models.FairScoreDoc(6,6,False),models.FairScoreDoc(5,5,True),
                                          models.FairScoreDoc(4,4,True),models.FairScoreDoc(3,3,False),
                                          models.FairScoreDoc(2,2,False),models.FairScoreDoc(1,1,False)]),
                         (20, 0.3, 0.1, [models.FairScoreDoc(20,20,False),models.FairScoreDoc(19,19,True),
                                         models.FairScoreDoc(18,18,False),models.FairScoreDoc(17,17,True),
                                         models.FairScoreDoc(16,16,True),models.FairScoreDoc(15,15,False),
                                         models.FairScoreDoc(14,14,False),models.FairScoreDoc(13,13,True),
                                         models.FairScoreDoc(12,12,False),models.FairScoreDoc(11,11,True),
                                         models.FairScoreDoc(10,10,False),models.FairScoreDoc(9,9,False),
                                         models.FairScoreDoc(8,8,True),models.FairScoreDoc(7,7,False),
                                         models.FairScoreDoc(6,6,False),models.FairScoreDoc(5,5,True),
                                         models.FairScoreDoc(4,4,True),models.FairScoreDoc(3,3,False),
                                         models.FairScoreDoc(2,2,False),models.FairScoreDoc(1,1,False)]),
))
def test_is_fair(k, p, alpha, ranking):
    f = fair.Fair(k, p, alpha)

    assert len(ranking) == k

    assert f.is_fair(ranking)


@pytest.mark.parametrize("k, p, alpha, result",(
            (10, 0.2, 0.15, [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]),
            (20, 0.25, 0.1, [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3]),
            (30, 0.3, 0.05, [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5])
))
def test_create_unadjusted_mtable(k, p, alpha, result):
    f = fair.Fair(k, p, alpha)

    mtable = f.create_unadjusted_mtable()

    assert mtable == result

@pytest.mark.parametrize("k, p, alpha, result",(
            (10, 0.2, 0.15, [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]),
            (20, 0.25, 0.1, [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2]),
            (30, 0.3, 0.05, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4])
))
def test_create_adjusted_mtable(k, p, alpha, result):
    f = fair.Fair(k, p, alpha)

    mtable = f.create_adjusted_mtable()

    assert mtable == result


@pytest.mark.parametrize("k, p, alpha, result",(
            (10, 0.2, 0.15, 0.15),
            (20, 0.25, 0.1, 0.07812500000000001),
            (30, 0.3, 0.15, 0.0796875)
))
def test_adjust_alpha(k, p, alpha, result):
    f = fair.Fair(k, p, alpha)

    adjusted_alpha = f.adjust_alpha()

    assert abs(adjusted_alpha - result) < 0.0001 # they should be same to the 5th decimal

@pytest.mark.parametrize("k, p, alpha, result",(
            (10, 0.2, 0.15, 0.13421772800000065),
            (20, 0.25, 0.1, 0.10515247355215251),
            (30, 0.3, 0.05, 0.04877730797178359)
))
def test_compute_fail_probability(k, p, alpha, result):
    f = fair.Fair(k, p, alpha)

    adjusted_mtable = f.create_adjusted_mtable()

    prob = f.compute_fail_probability(adjusted_mtable)

    assert abs(prob - result) < 0.0001  # they should be same to the 5th decimal


@pytest.mark.parametrize("k, p, alpha",(
            (10, 0.2, 0.15),
            (20, 0.25, 0.1),
            (30, 0.3, 0.05)
))
def test_mtable_generation(k, p, alpha):
    f = fair.Fair(k, p, alpha)

    # create an adjusted mtable with alpha unadjusted
    mtable = f.create_adjusted_mtable()

    # get alpha adjusted
    alpha_adjusted = f.adjust_alpha()

    # create a new unadjusted mtable with the new alpha
    f_adjusted = fair.Fair(k, p, alpha_adjusted)
    mtable_adjusted = f_adjusted.create_unadjusted_mtable()

    assert mtable == mtable_adjusted  # they should be same to the 5th decimal


@pytest.mark.parametrize("k, p, alpha, ranking",(
                         (20, 0.25, 0.1, [models.FairScoreDoc(20, 20, False), models.FairScoreDoc(19, 19, False),
                                         models.FairScoreDoc(18, 18, False), models.FairScoreDoc(17, 17, False),
                                         models.FairScoreDoc(16, 16, False), models.FairScoreDoc(15, 15, False),
                                         models.FairScoreDoc(14, 14, False), models.FairScoreDoc(13, 13, False),
                                         models.FairScoreDoc(12, 12, False), models.FairScoreDoc(11, 11, False),
                                         models.FairScoreDoc(10, 10, False), models.FairScoreDoc(9, 9, False),
                                         models.FairScoreDoc(8, 8, False), models.FairScoreDoc(7, 7, False),
                                         models.FairScoreDoc(6, 6, False), models.FairScoreDoc(5, 5, True),
                                         models.FairScoreDoc(4, 4, True), models.FairScoreDoc(3, 3, True),
                                         models.FairScoreDoc(2, 2, True), models.FairScoreDoc(1, 1, True)]),
                         (20, 0.3, 0.1, [models.FairScoreDoc(20,20,False),models.FairScoreDoc(19,19,False),
                                         models.FairScoreDoc(18,18,False),models.FairScoreDoc(17,17,False),
                                         models.FairScoreDoc(16,16,False),models.FairScoreDoc(15,15,False),
                                         models.FairScoreDoc(14,14,False),models.FairScoreDoc(13,13,False),
                                         models.FairScoreDoc(12,12,False),models.FairScoreDoc(11,11,True),
                                         models.FairScoreDoc(10,10,True),models.FairScoreDoc(9,9,False),
                                         models.FairScoreDoc(8,8,True),models.FairScoreDoc(7,7,False),
                                         models.FairScoreDoc(6,6,False),models.FairScoreDoc(5,5,True),
                                         models.FairScoreDoc(4,4,True),models.FairScoreDoc(3,3,True),
                                         models.FairScoreDoc(2,2,True),models.FairScoreDoc(1,1,True)]),
))
def test_re_rank(k, p, alpha, ranking):
    f = fair.Fair(k, p, alpha)

    re_ranked = f.re_rank(ranking)

    # input should not be fair
    assert not f.is_fair(ranking)

    # check length
    assert len(ranking) == len(re_ranked)

    # check content
    assert set([r.id for r in ranking]) == set([r.id for r in re_ranked])

    # output should be fair
    assert f.is_fair(re_ranked)
