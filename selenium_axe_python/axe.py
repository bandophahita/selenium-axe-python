# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Selenium Axe Python"""
from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver  # pragma: no cover
    from typing_extensions import TypeAlias

_DEFAULT_SCRIPT = os.path.join(os.path.dirname(__file__), "axe-core", "axe.min.js")

T_data: TypeAlias = Dict[str, List[Dict]]


class Axe:
    """Axe"""

    def __init__(self, selenium: WebDriver, script_url: str = _DEFAULT_SCRIPT):
        """
        script_url: location of the axe-core script.
        """
        self.script_url = script_url
        self.selenium = selenium

    def inject(self):
        """
        Recursively inject aXe into all iframes and the top level document.
        """
        with open(self.script_url, encoding="utf8") as f:
            self.selenium.execute_script(f.read())

    def run(self, context: object | None = None, options: Dict | None = None) -> T_data:
        """
        Run axe against the current page.

        :param context: which page part(s) to analyze and/or what to exclude.
        :param options: dictionary of aXe options.
        """
        args = ""

        # If context parameter is passed, add to args
        if context is not None:
            args += f"{context}"
            if options is not None:
                args += ","

        # If options parameter is passed, add to args
        if options is not None:
            args += f"{options}"

        command = (
            f"var callback = arguments[arguments.length - 1];"
            f"axe.run({args}).then(results => callback(results))"
        )
        response = self.selenium.execute_async_script(command)
        return response

    @staticmethod
    def report(violations: List[Dict]) -> str:
        """
        Return readable report of accessibility violations found.

        :param violations: Dictionary of violations.
        :return report: Readable report of violations.
        """
        string = ""
        string += f"Found {len(violations)} accessibility violations:"
        for violation in violations:
            string += (
                f"\n\n\nRule Violated:"
                f'\n{violation["id"]} - {violation["description"]}'
                f'\n\tURL: {violation["helpUrl"]}'
                f'\n\tImpact Level: {violation["impact"]}'
                f"\n\tTags:"
            )
            for tag in violation["tags"]:
                string += f" {tag}"
            string += "\n\tElements Affected:"
            i = 1
            for node in violation["nodes"]:
                for target in node["target"]:
                    string += f"\n\t{i}) Target: {target}"
                    i += 1
                for item in node["all"]:
                    string += f"\n\t\t{item['message']}"
                for item in node["any"]:
                    string += f"\n\t\t{item['message']}"
                for item in node["none"]:
                    string += f"\n\t\t{item['message']}"
            string += "\n\n\n"
        return string

    @staticmethod
    def write_results(data: Dict, name: str | None = None) -> None:
        """
        Write JSON to file with the specified name.

        :param name: Path to the file to be written to. If no path is passed
                     a new JSON file "results.json" will be created in the
                     current working directory.
        """

        if name:
            filepath = os.path.abspath(name)
        else:
            filepath = os.path.join(os.getcwd(), "results.json")

        with open(filepath, "w", encoding="utf8") as f:
            f.write(json.dumps(data, indent=4))
