import pytest

from fairsearchcore import simulator
from fairsearchcore import fair


@pytest.mark.parametrize("M, k, p, result",(
                         (100, 10, 0.25, 100),
                         (1000, 10, 0.2, 1000),
                         (5000, 30, 0.5, 5000),
                         (10000, 20, 0.3, 10000)))
def test_generate_rankings(M, k, p, result):
    allowed_offset = 0.02 # we tolerate an absolute difference in probability of 0.02

    # generate the rankings
    rankings = simulator.generate_rankings(M, k, p)

    # check if the size is right
    assert len(rankings) == result

    # check if the number of protected elements is right
    total = M * k
    protected = sum([sum([1 if rr.is_protected else 0 for rr in r]) for r in rankings])
    assert abs((protected * 1.0 / total) - p) < allowed_offset


def test_fail_probability_calcualtors():
    Ms = [1000, 10000]
    ks = [10, 20, 50, 100, 200]
    ps = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    alphas = [0.01, 0.05, 0.1, 0.15]

    allowed_offset = 0.02 # we tolerate an absolute difference in probability of 0.02

    for M in Ms:
        for k in ks:
            for p in ps:
                rankings = simulator.generate_rankings(M, k, p)
                for alpha in alphas:
                    f = fair.Fair(k, p, alpha)

                    mtable = f.create_adjusted_mtable()

                    experimental = simulator.compute_fail_probability(rankings, mtable)
                    analytical = f.compute_fail_probability(mtable)

                    # Not pretty, but adding all the parameters in the assert, so we know what combination fails
                    assert M > 0 and k > 0 and p > 0 and alpha > 0 \
                           and abs(experimental - analytical) < (allowed_offset + alpha * 0.01 / allowed_offset)
