#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from LimeSoup.RSCSoup import RSCSoup

__author__ = 'Ziqin (Shaun) Rong'
__maintainer__ = 'Ziqin (Shaun) Rong'
__email__ = 'rongzq08@gmail.com'


if __name__ == '__main__':
    html_str = "->"
    # Provide input interface to the html str, associated with the paper DOI index
    processed_json = RSCSoup.parse(html_str)
    print(processed_json)
