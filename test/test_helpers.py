# -*- coding: utf-8 -*-
from scrapy_tdd import *
from scrapy.http import Request, FormRequest
from scrapy import Item
import os
import pytest

def sample_file_path():
    return os.path.join(my_path(__file__), 'samples')

def describe_mock_response_creation():

    def describe_basic_operation():
        resp = mock_response_from_sample_file(sample_file_path(), "some_html_file.html",
                                              url="http://test.url", meta={"test": "key"})

        def it_creates_mock_responses():
            assert u"this is part of a mock HTML response" in resp.text
            assert b"this is part of a mock HTML response" in resp.body

        def it_reports_the_response_url():
            assert resp.url == "http://test.url"

        def it_passes_meta_params_along():
            assert resp.meta["test"] == "key"

    def it_tolerates_missing_protocol_and_defaults_to_http():
        resp = mock_response_from_sample_file(sample_file_path(), "some_html_file.html",
                                              url="test.url" )
        assert resp.url == "http://test.url"

    @pytest.mark.skip("needs to be implemented")
    def it_accepts__file__inplace_of_my_path():
        pass

    def describe_encoding_and_type_handling():
        @pytest.mark.skip("needs to be implemented")
        def it_detects_strange_encodings_based_on_html_tag():
            pass

        def it_loads_xml_files_properly_as_TextResponse():
            resp = mock_response_from_sample_file(sample_file_path(), "some_xml_file.xml",
                                                  url="test.url" )
            print(resp.__class__.__name__)
            assert isinstance(resp, TextResponse)

        def it_loads_json_files_properly_as_TextResponse():
            resp = mock_response_from_sample_file(sample_file_path(), "some_json_file.json",
                                                  url="test.url" )
            assert isinstance(resp, TextResponse)

        def it_loads_image_files_properly_as_Response():
            resp = mock_response_from_sample_file(sample_file_path(), "some_image_file.jpg",
                                                  url="test.url" )
            assert isinstance(resp, Response)

        def it_suspects_any_other_file_type_to_be_a_binary_and_loads_properly():
            resp = mock_response_from_sample_file(sample_file_path(), "some_binary_file.xyz",
                                                  url="test.url" )
            assert isinstance(resp, Response)


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
