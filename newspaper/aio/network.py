# -*- coding: utf-8 -*-
"""
All code involving requests and responses over the http network
must be abstracted in this file.
"""
__title__ = 'newspaper'
__author__ = '3liv & mhmerhi'
__license__ = 'MIT'
__copyright__ = 'Copyright 2019'

import logging
import requests

from newspaper.configuration import Configuration
from newspaper.mthreading import ThreadPool
from newspaper.settings import cj

from newspaper.network import _get_html_from_response
from newspaper.network import get_request_kwargs
from newspaper.network import *

import asyncio
import aiohttp
from aiohttp_requests import requests

log = logging.getLogger(__name__)


FAIL_ENCODING = 'ISO-8859-1'



async def get_html(url, config=None, response=None):
    """HTTP response code agnostic
    """
    try:
        return await get_html_2XX_only(url, config, response)
    except requests.exceptions.RequestException as e:
        log.debug('get_html() error. %s on URL: %s' % (e, url))
        return ''


async def get_html_2XX_only(url, config=None, response=None):
    """Consolidated logic for http requests from newspaper. We handle error cases:
    - Attempt to find encoding of the html by using HTTP header. Fallback to
      'ISO-8859-1' if not provided.
    - Error out if a non 2XX HTTP response code is returned.
    """
    config = config or Configuration()
    useragent = config.browser_user_agent
    timeout = config.request_timeout
    proxies = config.proxies
    headers = config.headers

    if response is not None:
        return _get_html_from_response(response)

    response = await requests.get(
        url=url, **get_request_kwargs(timeout, useragent, proxies, headers))

    html = _get_html_from_response(response)

    if config.http_success_only:
        # fail if HTTP sends a non 2XX response
        response.raise_for_status()

    return html


def multithread_request(urls, config=None):
    """Request multiple urls via mthreading, order of urls & requests is stable
    returns same requests but with response variables filled.
    """
    config = config or Configuration()
    num_threads = config.number_threads
    timeout = config.thread_timeout_seconds

    pool = ThreadPool(num_threads, timeout)

    m_requests = []
    for url in urls:
        m_requests.append(MRequest(url, config))

    for req in m_requests:
        pool.add_task(req.send)

    pool.wait_completion()
    return m_requests
