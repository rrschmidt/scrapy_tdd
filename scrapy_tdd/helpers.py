# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse, Request, XmlResponse, Response, TextResponse
from scrapy import Item
import os
import codecs

def my_path(file):
    return os.path.dirname(os.path.realpath(file))

def _read_textual_file(file_dir, partial_file_path, encoding):
    with codecs.open(os.path.join(file_dir, partial_file_path), encoding=encoding) as file:
        data = file.read()
    return data

def _read_binary_file(file_dir, partial_file_path):
    with open(os.path.join(file_dir, partial_file_path), mode="br") as file:
        data = file.read()
    return data

def mock_response_from_sample_file(file_dir, file_name,
                                   meta={}, url="http://fake_url.com",
                                   encoding='utf-8'):
    if "http" not in url: url = "http://" + url
    req = Request(url, meta=meta)
    if file_name.endswith(".xml"):
        body = _read_textual_file(file_dir, file_name, encoding=encoding)
        response = XmlResponse(url, body=body, request=req, encoding=encoding)
    elif file_name.endswith(".json"):
        body = _read_textual_file(file_dir, file_name, encoding=encoding)
        response = TextResponse(url, body=body, request=req, encoding=encoding)
    elif file_name.endswith(".html") or file_name.endswith(".htm"):
        body = _read_textual_file(file_dir, file_name, encoding=encoding)
        response = HtmlResponse(url, body=body, request=req, encoding=encoding)
    else:
        body = _read_binary_file(file_dir, file_name)
        response = Response(url, body=body, request=req)
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
