selenium-axe-python
===================

selenium-axe-python integrates aXe and selenium to enable automated web accessibility testing.

Originally created as [axe-selenium-python](http://github.com/mozilla-services/axe-selenium-python/) by [Kimberly Sereduck](https://github.com/kimberlythegeek).
Unfortunately she is no longer assigned to the project which means the original project has gone stale.
This is a fork of that project with some updates.

**This version of selenium-axe-python is using axe-core@4.7.2.**

[![License](https://img.shields.io/badge/license-MPL%202.0-blue.svg)](https://github.com/bandophahita/selenium-axe-python/blob/master/LICENSE.txt)
[![PyPI](https://img.shields.io/pypi/v/selenium-axe-python.svg)](https://pypi.org/project/selenium-axe-python/)
[![Supported Versions](https://img.shields.io/pypi/pyversions/screenpy.svg)](https://pypi.org/project/screenpy)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

[![Issues](https://img.shields.io/github/issues-raw/bandophahita/selenium-axe-python.svg)](https://github.com/bandophahita/selenium-axe-python/issues)

[![Build Status](https://github.com/bandophahita/selenium-axe-python/actions/workflows/tests.yml/badge.svg)](https://github.com/bandophahita/selenium-axe-python/actions/workflows/tests.yml)
[![Build Status](https://github.com/bandophahita/selenium-axe-python/actions/workflows/lint.yml/badge.svg)](https://github.com/bandophahita/selenium-axe-python/actions/workflows/lint.yml)

Requirements
------------

You will need the following prerequisites in order to use selenium-axe-python:

- selenium >= 3.0.2
- Python 3.11
- The appropriate driver for the browser you intend to use, downloaded and added to your path, e.g. geckodriver for Firefox:

  - [geckodriver](https://github.com/mozilla/geckodriver/releases) downloaded and [added to your PATH](https://stackoverflow.com/questions/40208051/selenium-using-python-geckodriver-executable-needs-to-be-in-path#answer-40208762)

Installation
------------

To install selenium-axe-python:

```bash
$ pip install selenium-axe-python
```

Usage
-----

```python

from selenium import webdriver
from selenium_axe_python import Axe


def test_google():
    driver = webdriver.Firefox()
    driver.get("http://www.google.com")
    axe = Axe(driver)
    # Inject axe-core javascript into page.
    axe.inject()
    # Run axe accessibility checks.
    results = axe.run()
    # Write results to file
    axe.write_results(results, 'a11y.json')
    driver.close()
    # Assert no violations are found
    assert len(results["violations"]) == 0, axe.report(results["violations"])
```

The method `axe.run()` accepts two parameters: `context` and `options`.

For more information on `context` and `options`, view the [aXe documentation here](https://github.com/dequelabs/axe-core/blob/master/doc/API.md#parameters-axerun).

Contributing
------------

You want to contribute? Great! Here are the things you should do before submitting your PR:


1. Fork the repo and git clone your fork.
1. `dev` install the project package:
    1. `pip install -e .[dev]`
    1. Optional (poetry users):
        1. `poetry install --extras dev`
1. Run `tox` to perform tests frequently.
1. Create pull-request from your branch.


The original project required you to run `npm install` (or in most cases did it at install for you) but this
limited the use of the package to systems that have npm.  This fork includes the latest version of
axe-core.

You can run the tests using [tox](https://tox.readthedocs.io/en/latest/):

```bash
$ tox
```

Alternatively you can use the makefile in the root of the repo:

```bash
$ make pre-check-in
```

Resources
---------

- [Issue Tracker](https://github.com/bandophahita/selenium-axe-python/issues)
- [Code](https://github.com/bandophahita/selenium-axe-python/)
- [pytest-axe](http://github.com/mozilla-services/pytest-axe/)

CHANGELOG
---------

## version 2.1.12

- forked from original repo [axe-selenium-python](http://github.com/mozilla-services/axe-selenium-python/)
- updated to work with python >=3.7


### version 2.1.5

**Breaks backwards compatibility**:

- The Axe class method `execute` has been renamed to `run` to mirror the method in the axe-core API.

### version 2.1.0

- Created package.json file to maintain axe-core dependency
- Replaced unit tests with more meaningful integration tests
  - included a sample html file for integration tests

### version 2.0.0

- All functionalities that are not part of axe-core have been moved into a separate package, `pytest-axe`. This includes:

  - `run_axe` helper method
  - `get_rules` Axe class method
  - `run` Axe class method
  - `impact_included` Axe class method
  - `analyze` Axe class method.

The purpose of this change is to separate implementations that are specific to the Mozilla Firefox Test Engineering team,
and leave the base `selenium-axe-python` package for a more broad use case. This package was modeled off of Deque's
Java package, axe-selenium-java, and will now more closely mirror it.

All functionalities can still be utilized when using `selenium-axe-python` in conjunction with `pytest-axe`.

### version 1.2.3

- Added the analyze method to the Axe class. This method runs accessibility checks, and writes the JSON results to file based on the page URL and the timestamp.
- Writing results to file can be enabled by setting the environment variable `ACCESSIBILITY_REPORTING=true`. The files will be written to `results/` directory, which must be created if it does not already exist.
- Accessibility checks can be disabled by setting the environment variable `ACCESSIBILITY_DISABLED=true`.

### version 1.2.1

- Updated axe to `axe-core@2.6.1`
- Modified impact_included class method to reflect changes to the aXe API:
- There are now only 3 impact levels: 'critical', 'serious', and 'minor'

### version 1.0.0

- Updated usage examples in README
- Added docstrings to methods lacking documentation
- Removed unused files

### version 0.0.3

- Added run method to Axe class to simplify the usage in existing test suites
- run method includes the ability to set what impact level to test for: 'minor', 'moderate', 'severe', 'critical'

### version 0.0.28

- Added selenium instance as a class attribute
- Changed file paths to OS independent structure
- Fixed file read operations to use with keyword


### version 0.0.21

- Fixed include of aXe API file and references to it
- Updated README
