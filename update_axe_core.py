#!/usr/bin/env python3
"""
Run this file to grab the latest version of the axe.min.js from axe-core
"""
from __future__ import annotations

from urllib.request import urlretrieve

file = "./selenium_axe_python/axe-core/axe.min.js"

rt = urlretrieve("https://unpkg.com/axe-core/axe.min.js", file)

with open(file) as fp:
    ver = fp.readline().split("v", maxsplit=1)[-1]

print(f"{ver}")
