#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from LimeSoup.lime_soup import Soup, RuleIngredient
from bs4 import BeautifulSoup

__author__ = 'Ziqin (Shaun) Rong'
__maintainer__ = 'Ziqin (Shaun) Rong'
__email__ = 'rongzq08@gmail.com'


# An example soup ingredient for RSC papers
class RSCRemoveCaption(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        # Remove captions from the HTML string
        html_str += 'remove caption '
        return html_str


# Another example soup ingredient for RSC papers
class RSCRemoveReferences(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        # Remove reference numbers from the HTML string
        html_str += " rscremovereference "
        return html_str


RSCSoup = Soup()
RSCSoup.add_ingredient(RSCRemoveCaption)
RSCSoup.add_ingredient(RSCRemoveReferences)
