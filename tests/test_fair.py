import pytest

from fairsearchcore import fair
from fairsearchcore import simulator

@pytest.mark.parametrize("k, p, alpha, ranking",(
                         (20, 0.25, 0.1, [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0]),
                         (20, 0.3, 0.1, [0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0]),
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


if __name__ == "__main__":
    k=20
    p=0.25
    alpha=0.1

    f = fair.Fair(k, p, alpha)

    adjusted_mtable = f.create_adjusted_mtable()

    M = 10000

    rankings = simulator.generate_rankings(M, k, p)

    print(simulator.compute_fail_probabilty(rankings, adjusted_mtable))