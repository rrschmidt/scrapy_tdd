scrapy_tdd
==========

Helpers and examples to build Scrapy Crawlers in a test driven way.

Motivation
----------

... coming soon ...

Why not scrapy's contracts?
---------------------------

... coming soon ...

Installation
============

``pip install scrapy_tdd``

Quick Start Examples
====================

    def describe_fancy_spider():
        to_test = MySpider().from_crawler(get_crawler())

        def describe_parse_suggested_terms():
            resp = response_from("Result_JSON_Widget.txt")
            results = to_test.parse(resp)

            def should_get_item():
                item = results
                assert item[0]["lorem"] == 'ipsum'
                assert item[0]["iterem"] == "ipsem"


Full Documentation
==================

... coming soon ...

Missing / next steps
====================

* Python 3.x compatibility
* Mocking Request-Response pairs

How to contribute
=================

... coming soon ...
