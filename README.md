selenium-axe-python
===================

selenium-axe-python integrates aXe and selenium to enable automated web accessibility testing.

Originally created as [axe-selenium-python](http://github.com/mozilla-services/axe-selenium-python/) by [Kimberly Sereduck](https://github.com/kimberlythegeek)
Unfortunately she is no longer assigned to the project which means the original project has gone stale.
This is basically a fork of that project with some updates.

**This version of selenium-axe-python is using axe-core@4.7.2.**

[![License](https://img.shields.io/badge/license-MPL%202.0-blue.svg)](https://github.com/mozilla-services/axe-selenium-python/blob/master/LICENSE.txt)
[![PyPI](https://img.shields.io/pypi/v/axe-selenium-python.svg)](https://pypi.org/project/axe-selenium-python/)
[![Travis](https://img.shields.io/travis/mozilla-services/axe-selenium-python.svg)](https://travis-ci.org/mozilla-services/axe-selenium-python)
[![Issues](https://img.shields.io/github/issues-raw/bandophahita/selenium-axe-python.svg)](https://github.com/bandophahita/selenium-axe-python/issues)


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
$ pip install git+https://github.com/bandophahita/selenium-axe-python
              git+ssh://git@github.com/bandophahita/selenium-axe-python.git@master
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

Fork the repository and submit PRs with bug fixes and enhancements;
contributions are very welcome.

~~Node dependencies must be installed by running `npm install` inside the selenium-axe-python directory~~

The original project required you to run `npm install` (or in most cases did it at install for you) but this
limited the use of the package to systems that have npm.  This fork includes the latest version of
axe-core.

You can run the tests using [tox](https://tox.readthedocs.io/en/latest/):

```bash
$ tox
```

Resources
---------

- [Issue Tracker](https://github.com/bandophahita/selenium-axe-python/issues)
- [Code](https://github.com/bandophahita/selenium-axe-python/)
- [pytest-axe](http://github.com/mozilla-services/pytest-axe/)

CHANGELOG
---------

## version 2.1.7

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
