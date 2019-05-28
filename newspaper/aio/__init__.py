# -*- coding: utf-8 -*-
"""
Ignore the unused imports, this file's purpose is to make visible
anything which a user might need to import from newspaper.
View newspaper/__init__.py for its usage.
"""
__title__ = 'newspaper'
__author__ = 'Ali V'
__license__ = 'MIT'
__copyright__ = 'Copyright 2019, Ali V'

import feedparser

from .article import Article
from ..configuration import Configuration
from ..settings import POPULAR_URLS, TRENDING_URL
from ..source import Source
from ..utils import extend_config, print_available_languages