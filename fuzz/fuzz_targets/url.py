#!/usr/bin/env python3

import atheris
import sys
import os

with atheris.instrument_imports():
    from requests_html import HTML
    from lxml.etree import ParserError

def TestOneInput(input):
    fdp = atheris.FuzzedDataProvider(input)
    
    length = fdp.ConsumeIntInRange(0, 4096)
    try:
        doc = HTML(url=fdp.ConsumeUnicodeNoSurrogates(length), html="<h1>Hello World</h1>")
    except ParserError:
        return

def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()

if __name__ == "__main__":
    main()