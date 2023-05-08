#!/usr/bin/env python3

import atheris
import sys
import os

with atheris.instrument_imports():
    from requests_html import HTML
    from lxml.etree import ParserError, XPathEvalError
    import unicodedata

def TestOneInput(input):
    fdp = atheris.FuzzedDataProvider(input)

    def remove_control(s):
        return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

    
    length = fdp.ConsumeIntInRange(0, 4096)
    try:
        doc = HTML(url="https://test.com", html=fdp.ConsumeUnicodeNoSurrogates(length))
        try:
            xpath = remove_control(fdp.ConsumeUnicodeNoSurrogates(fdp.ConsumeIntInRange(0, 128)))
            doc.xpath(xpath)
        except XPathEvalError:
            return
    except ParserError:
        return

def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()

if __name__ == "__main__":
    main()
