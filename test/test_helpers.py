# -*- coding: utf-8 -*-
from scrapy_tdd import *
from scrapy.http import Request, FormRequest
from scrapy import Item

import pytest

def describe_mock_response_creation():

    def it_creates_mock_responses():
        resp = mock_response_from_sample_file(my_path(__file__), "./test_helpers.py",
                                              url="http://test.url", meta={"test": "key"})
        assert resp.meta["test"] == "key"
        assert resp.url == "http://test.url"
        assert "it_creates_mock_responses" in resp.body

    def it_tolerates_missing_http():
        resp = mock_response_from_sample_file(my_path(__file__), "./test_helpers.py",
                                              url="test.url" )
        assert resp.url == "http://test.url"

    def it_tolerates_incomplete_paths():
        resp = mock_response_from_sample_file(my_path(__file__), "test_helpers.py", )
        assert "it_creates_mock_responses" in resp.body

def describe_request_result_handling():
    single_request = Request("http://test.com")
    mixed_requests = [ Request("http://test.com"), FormRequest("http://test2.com") ]
    complete_mix = mixed_requests + [ Item() ]

    def it_can_extract_request_objects():
        assert requests_in_parse_result([single_request]) == [single_request]

    def it_tolerates_None():
        assert requests_in_parse_result(None) == []
        assert items_in_parse_result(None) == []
        assert count_requests_in_parse_result(None) == 0
        assert count_items_in_parse_result(None) == 0

    def it_tolerates_single_elements():
        assert requests_in_parse_result(single_request) == [single_request]
        assert items_in_parse_result(single_request) == []

    def it_tolerates_and_sorts_out_items_mixed_in_between():
        assert requests_in_parse_result(complete_mix) == mixed_requests

    def it_tolerates_different_request_types():
        assert requests_in_parse_result(mixed_requests) == mixed_requests

    def it_extracts_urls_from_requests():
        urls = urls_from_requests(complete_mix)
        assert len(urls) == 2
        assert "http://test.com" in urls
        assert "http://test2.com" in urls

    def it_counts_the_requests_and_other_results():
        assert count_requests_in_parse_result(complete_mix) == 2
        assert count_items_in_parse_result(complete_mix) == 1

class MyItem(Item):
    pass

def describe_item_result_handling():
    single_item = Item()
    mixed_items = [ Item(), MyItem() ]
    complete_mix = mixed_items + [ Request("http://test.com") ]

    def it_can_extract_item_objects():
        assert items_in_parse_result([single_item]) == [single_item]

    def it_tolerates_single_elements():
        assert items_in_parse_result(single_item) == [single_item]
        assert requests_in_parse_result(single_item) == []

    def it_tolerates_items_mixed_in_between():
        assert items_in_parse_result(complete_mix) == mixed_items

    def it_tolerates_different_item_types():
        assert items_in_parse_result(mixed_items) == mixed_items

    def it_counts_the_items_and_other_results():
        assert count_requests_in_parse_result(complete_mix) == 1
        assert count_items_in_parse_result(complete_mix) == 2

def describe_url_counting():
    urls = ["http://test.com/page=1", "http://test.com/"]
    def it_counts_urls():
        assert count_urls_with("test.com", urls) == 2
        assert count_urls_with("page=1", urls) == 1
