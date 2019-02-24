# -*- coding: utf-8 -*-

"""
fairsearchcore.models
~~~~~~~~~~~~~~~
This module contains the primary objects that power fairsearchore.
"""


class FairScoreDoc(object):
    """The :class:`FairScoreDoc` object, which is a representation of the items in the rankings.
    Contains a `id`, `score` and `is_protected` attribute
    """

    def __init__(self, id, score, is_protected):
        self.id = id
        self.score = score
        self.is_protected = is_protected

    def __repr__(self):
        return "<FairScoreDoc [%s]>" % ("Protected" if self.is_protected else "Nonprotected")
