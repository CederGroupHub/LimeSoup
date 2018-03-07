#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import abc

__author__ = 'Ziqin (Shaun) Rong'
__maintainer__ = 'Ziqin (Shaun) Rong'
__email__ = 'rongzq08@gmail.com'


class SoupBase(object):
    """
    Act as the abstract class for rules and a publisher Parser
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """
        self._next points to the next parsing rule ingredient in the processing pipeline
        """
        self._next = None

    @abc.abstractmethod
    def parse(self, html_str):
        """
        :param html_str: raw HTML strings
        :return: Parse JSON object
        """
        raise NotImplementedError

    def add_ingredient(self, ingredient):
        """
        :param ingredient: A parsing rule ingredient concrete class
        """
        if self._next is not None:
            self._next.add_ingredient(ingredient)
        else:
            self._next = ingredient


class Soup(SoupBase):

    def __init__(self):
        super(Soup, self).__init__()

    def parse(self, html_str):
        if not self._next:
            raise ValueError("Please provide at least one parsing rule ingredient to the soup")
        return self._next.parse(html_str)


class RuleIngredient(SoupBase):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(RuleIngredient, self).__init__()

    def parse(self, html_str):
        results = self._parse(html_str)
        if self._next:
            results = self._next.parse(results)
        return results

    @staticmethod
    @abc.abstractmethod
    def _parse(html_str):
        """
        :param html_str: raw HTML strings
        :return: Parse JSON object
        """
        raise NotImplementedError
