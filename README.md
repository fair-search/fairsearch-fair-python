# Fair search core for Python

[![image](https://img.shields.io/pypi/status/fairsearchcore.svg)](https://pypi.org/project/fairsearchcore/)
[![image](https://img.shields.io/pypi/v/fairsearchcore.svg)](https://pypi.org/project/fairsearchcore/)
[![image](https://img.shields.io/pypi/pyversions/fairsearchcore.svg)](https://pypi.org/project/fairsearchcore/)
[![image](https://img.shields.io/pypi/l/fairsearchcore.svg)](https://pypi.org/project/fairsearchcore/)
[![image](https://img.shields.io/pypi/implementation/fairsearchcore.svg)](https://pypi.org/project/fairsearchcore/)

This is the Python library with the core algorithms used to do [FA*IR](https://arxiv.org/abs/1706.06368) ranking.  

## Installation
To install `fairsearchcore`, simply use `pip` (or `pipenv`):
```bash
pip install fairsearchcore
```
And, that's it!

## Using it in your code
You need to import the package first: 
```python
import fairsearchcore as fsc
```
Creating and analyzing mtables:
```python
k = 20 # number of topK elements returned (value should be between 10 and 400)
p = 0.25 # proportion of protected candidates in the topK elements (value should be between 0.02 and 0.98) 
alpha = 0.1 # significance level (value should be between 0.01 and 0.15)

# create the Fair object 
fair = fsc.Fair(k, p, alpha)

# create an mtable using alpha unadjusted
mtable = fair.create_unadjusted_mtable()
>> [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3]

# analytically calculate the fail probability
analytical = fair.compute_fail_probability(mtable)
>> 0.11517506930977106 

# create an mtable using alpha adjusted
mtable = fair.create_adjusted_mtable()
>> [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2]

# again, analytically calculate the fail probability
analytical = fair.compute_fail_probability(mtable)
>> 0.10515247355215251

```
Generate random rankings and analyze them:
```python
M = 10000 # number of rankings you want to generate (works better with big numbers)

# generate rankings using the simulator (M lists of k objects of class fairsearchcore.models.FairScoreDoc) 
rankings = fsc.generate_rankings(M, k, p)
>> [[<FairScoreDoc [Protected]>, <FairScoreDoc [Nonprotected]>, <FairScoreDoc [Protected]>, 
<FairScoreDoc [Protected]>, <FairScoreDoc [Nonprotected]>, <FairScoreDoc [Nonprotected]>, 
<FairScoreDoc [Nonprotected]>, <FairScoreDoc [Protected]>, <FairScoreDoc [Nonprotected]>, 
<FairScoreDoc [Nonprotected]>, <FairScoreDoc [Nonprotected]>, <FairScoreDoc [Nonprotected]>, 
<FairScoreDoc [Nonprotected]>, <FairScoreDoc [Protected]>, <FairScoreDoc [Nonprotected]>, 
 <FairScoreDoc [Nonprotected]>, <FairScoreDoc [Nonprotected]>, <FairScoreDoc [Nonprotected]>, 
 <FairScoreDoc [Nonprotected]>, <FairScoreDoc [Protected]>],...]

# experimentally calculate the fail probability
experimental = fsc.compute_fail_probability(rankings, mtable)
>> 0.1025
```
Let's get the alpha adjusted (used to create an adjusted mtable)
```python
# get alpha adjusted
alpha_adjusted = fair.adjust_alpha()
>> 0.07812500000000001
```
Apply a fair re-ranking to a given ranking:
```python
# import the FairScoreDoc class
from fairsearchcore.models import FairScoreDoc

# let's manually create an unfair ranking (False -> unprotected, True -> protected)
# in this example the first document (docid=20) has a score of 20, the last document (docid=1) a score of 1
unfair_ranking = [FairScoreDoc(20, 20, False), FairScoreDoc(19, 19, False), FairScoreDoc(18, 18, False),
                      FairScoreDoc(17, 17, False), FairScoreDoc(16, 16, False), FairScoreDoc(15, 15, False),
                      FairScoreDoc(14, 14, False), FairScoreDoc(13, 13, False), FairScoreDoc(12, 12, False),
                      FairScoreDoc(11, 11, False), FairScoreDoc(10, 10, False), FairScoreDoc(9, 9, False),
                      FairScoreDoc(8, 8, False), FairScoreDoc(7, 7, False), FairScoreDoc(6, 6, True),
                      FairScoreDoc(5, 5, True), FairScoreDoc(4, 4, True), FairScoreDoc(3, 3, True),
                      FairScoreDoc(2, 2, True), FairScoreDoc(1, 1, True)]
                      
# let's check the ranking is considered fair
fair.is_fair(unfair_ranking)
>> False

# now re-rank the unfair ranking                 
re_ranked = fair.re_rank(unfair_ranking)
>> [<FairScoreDoc [Nonprotected]>, <FairScoreDoc [Nonprotected]>, <FairScoreDoc [Nonprotected]>, 
<FairScoreDoc [Nonprotected]>, <FairScoreDoc [Nonprotected]>, <FairScoreDoc [Nonprotected]>, 
<FairScoreDoc [Nonprotected]>, <FairScoreDoc [Nonprotected]>, <FairScoreDoc [Protected]>, 
<FairScoreDoc [Nonprotected]>, <FairScoreDoc [Nonprotected]>, <FairScoreDoc [Nonprotected]>, 
<FairScoreDoc [Nonprotected]>, <FairScoreDoc [Nonprotected]>, <FairScoreDoc [Nonprotected]>,
<FairScoreDoc [Protected]>, <FairScoreDoc [Protected]>, <FairScoreDoc [Protected]>, 
<FairScoreDoc [Protected]>, <FairScoreDoc [Protected]>]

# now let's see if the new ranking is fair
fair.is_fair(re_ranked)
>> True

```

The library contains sufficient code documentation for each of the functions.
 
## Development

1. Clone this repository `git clone https://github.com/fair-search/fairsearchcore-python.git`
2. Change directory to the directory where you cloned the repository `cd WHERE_ITS_DOWNLOADED/fairsearchcore-python`
3. Use any IDE to work with the code

## Testing

Just run:
```
python setup.py test 
```
*Note*: The simulator tests take a *looong* time to execute. Also, because there is a *randomness* factor involved in 
the tests, it can happen that (rarely) they fail sometimes.
## Credits

The FA*IR algorithm is described on this paper:

* Meike Zehlike, Francesco Bonchi, Carlos Castillo, Sara Hajian, Mohamed Megahed, Ricardo Baeza-Yates: "[FA*IR: A Fair Top-k Ranking Algorithm](https://doi.org/10.1145/3132847.3132938)". Proc. of the 2017 ACM on Conference on Information and Knowledge Management (CIKM).

This code was developed by [Ivan Kitanovski](http://ivankitanovski.com/) based on the paper. See the [license](https://github.com/fair-search/fairsearchcore-python/blob/master/LICENSE) file for more information. For any questions contact [Mieke Zehlike].(https://de.linkedin.com/in/meike-zehlike-366bba131)

## See also

You can also see the [FA*IR plug-in for ElasticSearch](https://github.com/fair-search/fairsearch-fair-for-elasticsearch)
and and [FA*IR search core Java library](https://github.com/fair-search/fairsearch-fair-java).
