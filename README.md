# Fair search core for Python

This is the Python library with the core algorithms used to do [FA*IR](https://arxiv.org/abs/1706.06368) ranking.  

## Installation
To install `fairsearchcore`, simply use `pip` (or `pipenv`):
```bash
pip install fairsearcore
```
And, that's it!

# Using it in your code
You need to import the package first: 
```{.sourceCode .python}
import fairsearchcore as fsc
```
Creating and analyzing mtables:
```{.sourceCode .python}
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
>> 0.13421772800000065

```
Generate random rankings and analyze them:
```{.sourceCode .python}
M = 10000 # number of rankings you want to generate (works better with big numbers)

# generate rankings using the simulator (generates M lists of k items) 
rankings = fsc.generate_rankings(M, k, p)
>> [[0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],...]

# experimentally calculate the fail probability
experimental = fsc.compute_fail_probability(mtable, rankings)
>> 0.1076
```

The library contains sufficient code documentation for each of the functions.
 
## Development

1. Clone this repository `git clone https://github.com/fair-search/fairsearch-core.git`
2. Change directory to the directory where you cloned the repository `cd WHERE_ITS_DOWNLOADED/fairsearch-core/python`
3. Use any IDE to work with the code

## Testing

## Credits

The FA*IR algorithm is described on this paper:

* Meike Zehlike, Francesco Bonchi, Carlos Castillo, Sara Hajian, Mohamed Megahed, Ricardo Baeza-Yates: "[FA*IR: A Fair Top-k Ranking Algorithm](https://doi.org/10.1145/3132847.3132938)". Proc. of the 2017 ACM on Conference on Information and Knowledge Management (CIKM).

This code was developed by (Ivan Kitanovski)[http://ivankitanovski.com/] based on the paper. See the [license](https://github.com/fair-search/fairsearch-core/blob/master/python/LICENSE) file for more information.

## See also

See also: [FA*IR plug-in for ElasticSearch](https://github.com/fair-search/fairsearch-elasticsearch-plugin)
