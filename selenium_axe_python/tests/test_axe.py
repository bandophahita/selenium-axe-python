from __future__ import annotations

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
import json
import os
from typing import TYPE_CHECKING, Any, Union

import pytest
from setup_selenium import Browser, SetupSelenium
from typing_extensions import TypeAlias

from ..axe import Axe

if TYPE_CHECKING:
    from collections.abc import Generator

    from py._path.local import LocalPath
    from pytest_mock import MockerFixture
    from selenium.webdriver import Chrome, Edge, Firefox, Ie, Safari
    from selenium.webdriver.remote.webdriver import WebDriver

    AnyDriver: TypeAlias = Union[Chrome, Firefox, Safari, Ie, Edge]

_DEFAULT_TEST_FILE = os.path.join(os.path.dirname(__file__), "test_page.html")


@pytest.fixture()
def firefox_driver() -> Generator[WebDriver, Any, None]:
    enable_log_driver = False
    log_dir: str = "./logs"
    driver_path: str | None = None

    driver: AnyDriver = SetupSelenium.create_driver(
        browser=Browser.FIREFOX,
        headless=True,
        enable_log_driver=enable_log_driver,
        log_dir=log_dir,
        driver_path=driver_path,
    )
    yield driver
    driver.close()


@pytest.fixture()
def chrome_driver() -> Generator[WebDriver, Any, None]:
    enable_log_driver = False
    log_dir: str = "./logs"
    driver_path = os.getenv("CHROMEDRIVER_PATH")

    driver: AnyDriver = SetupSelenium.create_driver(
        browser=Browser.CHROME,
        headless=True,
        enable_log_driver=enable_log_driver,
        log_dir=log_dir,
        driver_path=driver_path,
    )
    yield driver
    driver.close()


def confirm_data(data: dict) -> None:
    assert len(data["inapplicable"]) == 74
    assert len(data["incomplete"]) == 0
    assert len(data["passes"]) == 6
    assert len(data["violations"]) == 9


@pytest.mark.nondestructive
def test_run_axe_sample_page_firefox(firefox_driver: WebDriver) -> None:
    """Run axe against sample page and verify JSON output is as expected."""
    data = _perform_axe_run(firefox_driver)

    confirm_data(data)


@pytest.mark.nondestructive
def test_run_axe_sample_page_chrome(chrome_driver: WebDriver) -> None:
    """Run axe against sample page and verify JSON output is as expected."""
    data = _perform_axe_run(chrome_driver)

    confirm_data(data)


def test_run(chrome_driver: WebDriver) -> None:
    driver = chrome_driver
    driver.get("file://" + _DEFAULT_TEST_FILE)
    axe = Axe(driver)
    axe.inject()
    data1 = axe.run(
        options={
            "runOnly": {
                "type": "rule",
                "values": [
                    "html-has-lang",
                ],
            }
        }
    )
    data2 = axe.run(context="['select']")
    data3 = axe.run(
        context=["html"],
        options={
            "runOnly": {
                "type": "rule",
                "values": [
                    "html-has-lang",
                    "document-title",
                ],
            }
        },
    )

    assert len(data1["inapplicable"]) == 0
    assert len(data1["incomplete"]) == 0
    assert len(data1["passes"]) == 0
    assert len(data1["violations"]) == 1

    assert len(data2["inapplicable"]) == 82
    assert len(data2["incomplete"]) == 0
    assert len(data2["passes"]) == 4
    assert len(data2["violations"]) == 1

    assert len(data3["inapplicable"]) == 0
    assert len(data3["incomplete"]) == 0
    assert len(data3["passes"]) == 0
    assert len(data3["violations"]) == 2


def _perform_axe_run(driver: WebDriver) -> dict:
    driver.get("file://" + _DEFAULT_TEST_FILE)
    axe = Axe(driver)
    axe.inject()
    return axe.run()


def test_write_results_to_file(tmpdir: LocalPath, mocker: MockerFixture) -> None:
    axe = Axe(mocker.MagicMock())
    data = {"testKey": "testValue"}
    filename = os.path.join(str(tmpdir), "manual_results.json")

    axe.write_results(data, filename)

    with open(filename) as f:
        actual_file_contents = json.loads(f.read())

    assert data == actual_file_contents


def test_write_results_without_filepath(mocker: MockerFixture) -> None:
    axe = Axe(mocker.MagicMock())
    data = {"testKey": "testValue"}
    cwd = os.getcwd()
    filename = os.path.join(cwd, "results.json")

    axe.write_results(data)
    with open(filename) as f:
        actual_file_contents = json.loads(f.read())

    assert data == actual_file_contents
    assert os.path.dirname(filename) == cwd


@pytest.mark.nondestructive
def test_report() -> None:
    """Run axe against sample page and verify text output is as expected."""

    violation = [
        {
            "description": (
                "Ensures each HTML document contains a non-empty <title> element"
            ),
            "help": "Documents must have <title> element to aid in navigation",
            "helpUrl": "https://dequeuniversity.com/rules/axe/4.7/document-title?application=axeAPI",
            "id": "document-title",
            "impact": "serious",
            "nodes": [
                {
                    "all": [],
                    "any": [
                        {
                            "data": None,
                            "id": "doc-has-title",
                            "impact": "serious",
                            "message": "Document does not have a non-empty <title> element",
                            "relatedNodes": [],
                        }
                    ],
                    "failureSummary": (
                        "Fix any of the following:\n  "
                        "Document does not have a non-empty <title> element"
                    ),
                    "html": "<html>",
                    "impact": "serious",
                    "none": [],
                    "target": ["html"],
                }
            ],
            "tags": [
                "cat.text-alternatives",
                "wcag2a",
                "wcag242",
                "ACT",
                "TTv5",
                "TT12.a",
            ],
        },
        {
            "description": "Ensures every HTML document has a lang attribute",
            "help": "<html> element must have a lang attribute",
            "helpUrl": "https://dequeuniversity.com/rules/axe/4.7/html-has-lang"
            "?application=axeAPI",
            "id": "html-has-lang",
            "impact": "serious",
            "nodes": [
                {
                    "all": [],
                    "any": [
                        {
                            "data": {"messageKey": "noLang"},
                            "id": "has-lang",
                            "impact": "serious",
                            "message": "The <html> element does not have a lang attribute",
                            "relatedNodes": [],
                        }
                    ],
                    "failureSummary": "Fix any of the following:\n  The <html> element does not have a lang attribute",
                    "html": "<html>",
                    "impact": "serious",
                    "none": [],
                    "target": ["html"],
                }
            ],
            "tags": ["cat.language", "wcag2a", "wcag311", "ACT", "TTv5", "TT11.a"],
        },
        {
            "description": "Ensures the document has a main landmark",
            "help": "Document should have one main landmark",
            "helpUrl": "https://dequeuniversity.com/rules/axe/4.7/landmark-one-main"
            "?application=axeAPI",
            "id": "landmark-one-main",
            "impact": "moderate",
            "nodes": [
                {
                    "all": [
                        {
                            "data": None,
                            "id": "page-has-main",
                            "impact": "moderate",
                            "message": "Document does not have a main landmark",
                            "relatedNodes": [],
                        }
                    ],
                    "any": [],
                    "failureSummary": "Fix all of the following:\n  Document does not have a main landmark",
                    "html": "<html>",
                    "impact": "moderate",
                    "none": [],
                    "target": ["html"],
                }
            ],
            "tags": ["cat.semantics", "best-practice"],
        },
        {
            "description": "Ensures that lists are structured correctly",
            "help": "<ul> and <ol> must only directly contain <li>, <script> or "
            "<template> elements",
            "helpUrl": "https://dequeuniversity.com/rules/axe/4.7/list?application"
            "=axeAPI",
            "id": "list",
            "impact": "serious",
            "nodes": [
                {
                    "all": [],
                    "any": [],
                    "failureSummary": "Fix "
                    "all "
                    "of "
                    "the "
                    "following:\n  List element has direct children that are not allowed: div",
                    "html": "<ul>\n      "
                    "<div>\n        "
                    "<li>This is a "
                    "line "
                    "element</li>\n  "
                    "    </div>\n    "
                    "</ul>",
                    "impact": "serious",
                    "none": [
                        {
                            "data": {"values": "div"},
                            "id": "only-listitems",
                            "impact": "serious",
                            "message": "List element has direct children that are not allowed: div",
                            "relatedNodes": [
                                {
                                    "html": "<div>\n        <li>This is a line element</li>\n      </div>",
                                    "target": ["div"],
                                }
                            ],
                        }
                    ],
                    "target": ["ul"],
                }
            ],
            "tags": ["cat.structure", "wcag2a", "wcag131"],
        },
    ]
    output = Axe.report(violation)

    expected = """Found 4 accessibility violations:


Rule Violated:
document-title - Ensures each HTML document contains a non-empty <title> element
	URL: https://dequeuniversity.com/rules/axe/4.7/document-title?application=axeAPI
	Impact Level: serious
	Tags: cat.text-alternatives wcag2a wcag242 ACT TTv5 TT12.a
	Elements Affected:
	1) Target: html
		Document does not have a non-empty <title> element





Rule Violated:
html-has-lang - Ensures every HTML document has a lang attribute
	URL: https://dequeuniversity.com/rules/axe/4.7/html-has-lang?application=axeAPI
	Impact Level: serious
	Tags: cat.language wcag2a wcag311 ACT TTv5 TT11.a
	Elements Affected:
	1) Target: html
		The <html> element does not have a lang attribute





Rule Violated:
landmark-one-main - Ensures the document has a main landmark
	URL: https://dequeuniversity.com/rules/axe/4.7/landmark-one-main?application=axeAPI
	Impact Level: moderate
	Tags: cat.semantics best-practice
	Elements Affected:
	1) Target: html
		Document does not have a main landmark





Rule Violated:
list - Ensures that lists are structured correctly
	URL: https://dequeuniversity.com/rules/axe/4.7/list?application=axeAPI
	Impact Level: serious
	Tags: cat.structure wcag2a wcag131
	Elements Affected:
	1) Target: ul
		List element has direct children that are not allowed: div


"""

    assert output == expected
