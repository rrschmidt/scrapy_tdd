# -*- coding: utf-8 -*-
import os
import codecs
import scrapy
import mimetypes
from scrapy import Item
from http.cookies import SimpleCookie
from scrapy.http import Request, Response, HtmlResponse, XmlResponse, TextResponse, Headers


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
                                   encoding='utf-8', headers=None, cookies=None):
    if "http" not in url:
        url = "http://" + url
    req = Request(url, meta=meta)

    if _is_textual_file(file_name):
        body = _read_textual_file(file_dir, file_name, encoding=encoding)
    else:
        body = _read_binary_file(file_dir, file_name)

    if _is_xml_like_file(file_name):
        response = XmlResponse(url, body=body, request=req, encoding=encoding)
        deduced_content_type = 'application/xml'
    elif _is_html_like_file(file_name):
        response = HtmlResponse(url, body=body, request=req, encoding=encoding)
        deduced_content_type = 'text/html'
    elif _is_other_text_like_file(file_name):
        response = TextResponse(url, body=body, request=req, encoding=encoding)
        deduced_content_type = 'text/plain'
    else:
        mime_type, encoding = mimetypes.guess_type(file_name)
        response = Response(url, body=body, request=req)
        deduced_content_type = mime_type if mime_type else 'application/octet-stream'

    response.headers = Headers()
    response.headers.update(headers or {})
    response.headers.update({'Content-Type': deduced_content_type})

    if cookies:
        cookie = SimpleCookie()
        for key, value in cookies.items():
            cookie[key] = value
        cookie_header = cookie.output(header='', sep=',').strip()
        response.headers.update({"Set-Cookie": cookie_header})

    return response


def _is_textual_file(filename):
    return _is_xml_like_file(filename) or _is_html_like_file(filename) or _is_other_text_like_file(filename)


def _is_xml_like_file(filename):
    return filename.endswith(".xml")


def _is_html_like_file(filename):
    return _str_endswith_any(filename, [".html", ".htm"])


def _is_other_text_like_file(filename):
    return _str_endswith_any(filename, [".json", ".txt"])


def _str_endswith_any(text, accepted_ends):
    # TODO: likely can be done nicer with a neat regex
    for accepted_end in accepted_ends:
        if text.endswith(accepted_end):
            return True
    return False


def urls_from_requests(results):
    return set([r.url for r in requests_in_parse_result(results)])


def requests_in_parse_result(results):
    if results == None:
        return []
    if _is_single_element(results):
        return _type_in_parse_results([results], Request)
    else:
        return _type_in_parse_results(results, Request)


def items_in_parse_result(results):
    if results == None:
        return []
    if _is_single_element(results):
        return _type_in_parse_results([results], Item)
    else:
        return _type_in_parse_results(results, Item)


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
        if part in url:
            counter += 1
    return counter
