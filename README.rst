
.. image:: https://travis-ci.org/rrschmidt/scrapy_tdd.svg?branch=master
    :target: https://travis-ci.org/rrschmidt/scrapy_tdd

.. image:: https://codeclimate.com/github/codeclimate/codeclimate/badges/coverage.svg
   :target: https://codeclimate.com/github/rrschmidt/scrapy_tdd/coverage
   :alt: Test Coverage

scrapy_tdd
==========

Helpers and examples to build Scrapy Crawlers in a test driven way.

Motivation / Why should I develop Scrapy Crawlers using TDD?
------------------------------------------------------------

#. The develop - test cycle goes down to a few seconds and so it allows you to get a properly
   working scraper up much faster
#. When bugs are discovered in "the wild" with real data, new example files, a test and a fix can be created and tested
   much faster
#. It allows for fast refactoring without breaking anything - which results in much cleaner scraper code
#. It just feels right when you are used to be doing TDD

What's the difference to Scrapy's Spiders Contracts?
----------------------------------------------------

Scrapy has its own builtin testing feature named `Spiders Contracts <https://doc.scrapy.org/en/latest/topics/contracts.html>`_

I tried to use them for some time, but decided to build real unit tests in a unit test framework like py.test because
of these shortcomings:

- its philosophy is geared towards testing against contracts (thus the name) that by nature are more broad and less
  specific concepts. Testing for exact field contents in items can be done, but is difficult and fragile
- its documentation and basic set of features is a bit thin
- it mixes implementation code with contract descriptions which is only usable when there are few and simple contracts


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

* Mocking Request-Response pairs

How to contribute
=================

... coming soon ...
