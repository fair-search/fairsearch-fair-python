# -*- coding: utf-8 -*-

"""
---------------------------------------
Fair search core for Python
---------------------------------------

This is the Python library with the core algorithms used to do FA*IR ranking.


For details on support methods - see `fairsearchcore.fair` and `fairsearchcore.simulator`. Full documentation
is at https://github.com/fair-search/fairsearch-core/tree/master/python.

:copyright: (c) 2019 by Ivan Kitanovski
:license: Apache 2.0, see LICENSE for more details.
"""
from .fair import check_ranking, Fair
from .simulator import compute_fail_probability, generate_rankings

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())