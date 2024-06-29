A Python function that accepts a user agent string (and, optionally,
``Sec-CH-UA`` and ``Sec-CH-UA-Platform`` headers) and returns its best guess at
the browser name, version, and platform.

Motivation
==========

I wanted to be able to tell users all of the devices they were logged in on,
and I wanted the information being displayed to be as accurate as possible.

While looking for a solution, I learned that using just a user agent string was
not enough and neither was using just client hints.

For more information, see https://github.com/ua-parser/uap-core/issues/452

Why Is Using Just a User Agent String Not Enough?
=================================================

Sometimes browsers identify themselves in their ``Sec-CH-UA`` header but not
their user agent string. Brave is an example of this (except for the iOS
version, which does not send ``Sec-CH-UA`` or ``Sec-CH-UA-Platform`` headers).

Why Is Using Just Client Hints Not Enough?
==========================================

Sometimes browsers identify themselves in their user agent string but not their
``Sec-CH-UA`` header. The Android version of Ecosia is an example of this (its
``Sec-CH-UA`` header says that it is Chromium). In addition, some browsers do
not send ``Sec-CH-UA`` or ``Sec-CH-UA-Platform`` headers.

Installation
============

.. code-block:: bash

    pip install identify_browser

Usage
=====

.. code-block:: python

    from identify_browser import identify_browser

    # These values could come from anywhere. For example, in Django, they could come from:
    #
    # request.headers.get("User-Agent", "")
    # request.headers.get("Sec-Ch-Ua", "")
    # request.headers.get("Sec-Ch-Ua-Platform", "")
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    sec_ch_ua = '"Not/A)Brand";v="8", "Chromium";v="126", "Brave";v="126"'
    sec_ch_ua_platform = '"Windows"'

    browser_identity = identify_browser(user_agent, sec_ch_ua, sec_ch_ua_platform)
    print(f"You appear to be using {browser_identity['name']} {browser_identity['version']} on {browser_identity['platform']}")
    # Output: You appear to be using Brave 126 on Windows
