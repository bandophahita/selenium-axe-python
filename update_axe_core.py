#!/usr/bin/env python3
"""
Run this jsfile to grab the latest version of the axe.min.js from axe-core
"""
from __future__ import annotations

from urllib.request import urlretrieve

jsfile = "./selenium_axe_python/axe-core/axe.min.js"
verfile = "./selenium_axe_python/axe-core/version.txt"

rt = urlretrieve("https://unpkg.com/axe-core/axe.min.js", jsfile)

with open(jsfile) as fp:
    ver = fp.readline().split("v", maxsplit=1)[-1].strip()

with open(verfile, "w") as fp:
    fp.write(ver)


ver_line = "**This version of selenium-axe-python is using axe-core@"
new_line = f"**This version of selenium-axe-python is using axe-core@{ver}**\n"


readmelines=open("README.md").readlines()
with open("README.md", "w") as fp:
    for line in readmelines:
        if ver_line in line and new_line != line:
            print(f"Replacing:\n\t{line}\nwith:\n\t{new_line}")
            fp.write(new_line)
        else:
            fp.write(line)
