# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse, Request
from scrapy import Item
import os

def my_path(file):
    return os.path.dirname(os.path.realpath(file))

def _read_text_fixture(file_dir, partial_file_path):
    with open(os.path.join(file_dir, partial_file_path)) as file:
        data = file.read()
    return data

def mock_response_from_sample_file(file_dir, file_name,
                                   meta={}, url="http://fake_url.com"):
    if "http" not in url: url = "http://" + url
    html = _read_text_fixture(file_dir, file_name)
    req = Request(url, meta=meta)
    response = HtmlResponse(url, body = html, request=req)
    return response


def urls_from_requests(results):
    return set([ r.url for r in requests_in_parse_result(results) ])

def requests_in_parse_result(results):
    if results == None: return []
    if _is_single_element(results): return _type_in_parse_results([results], Request)
    else: return _type_in_parse_results(results, Request)

def items_in_parse_result(results):
    if results == None: return []
    if _is_single_element(results): return _type_in_parse_results([results], Item)
    else: return _type_in_parse_results(results, Item)

def _is_single_element(element):
    # can't look for iterables etc as items are iterable itself
    return isinstance(element, Item) or isinstance(element, Request)

def _type_in_parse_results(results, type):
    cleaned = []
    for result in results:
        if isinstance(result, type):
            cleaned.append(result)
    return cleaned

def count_items_in_parse_result(results):
    return len(items_in_parse_result(results))

def count_requests_in_parse_result(results):
    return len(requests_in_parse_result(results))

def count_urls_with(part, urls):
    counter = 0
    for url in urls:
        if part in url: counter += 1
    return counter
