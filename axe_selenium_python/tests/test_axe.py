# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from ..axe import Axe

_DEFAULT_TEST_FILE = os.path.join(os.path.dirname(__file__), "test_page.html")


@pytest.fixture
def firefox_driver():
    enable_log_driver = False
    log_dir: str = "./logs"
    driver_path: str | None = None

    options = webdriver.FirefoxOptions()
    options.set_capability("unhandledPromptBehavior", "ignore")

    # profile settings
    options.set_preference("app.update.auto", False)
    options.set_preference("app.update.enabled", False)
    options.set_preference("network.prefetch-next", False)
    options.set_preference("network.dns.disablePrefetch", True)
    options.add_argument("--headless")

    logpath = "/dev/null"
    options.log.level = "fatal"  # type: ignore[assignment]
    if enable_log_driver:
        lp = os.path.abspath(os.path.expanduser(log_dir))
        logpath = os.path.join(lp, "geckodriver.log")

    if driver_path:
        service = FirefoxService(executable_path=driver_path, log_path=logpath)
    else:
        service = FirefoxService(log_path=logpath)

    driver = webdriver.Firefox(service=service, options=options)
    yield driver
    driver.close()


@pytest.fixture
def chrome_driver():
    enable_log_driver = False
    log_dir: str = "./logs"

    opts = (
        "--disable-extensions",
        "--allow-running-insecure-content",
        "--ignore-certificate-errors",
        "--disable-single-click-autofill",
        "--disable-autofill-keyboard-accessory-view[8]",
        "--disable-full-form-autofill-ios",
        # https://bugs.chromium.org/p/chromedriver/issues/detail?id=402#c128
        # "--dns-prefetch-disable",
        "--disable-infobars",
        # chromedriver crashes without these two in linux
        "--no-sandbox",
        "--disable-dev-shm-usage",
    )

    options = webdriver.ChromeOptions()
    for opt in opts:
        options.add_argument(opt)

    options.headless = True
    driver_path = os.getenv("CHROMEDRIVER_PATH")

    logging_prefs = {"browser": "OFF", "performance": "OFF", "driver": "OFF"}

    args: list | None = None
    logpath = None
    if enable_log_driver:
        lp = os.path.abspath(os.path.expanduser(log_dir))
        logpath = os.path.join(lp, "chromedriver.log")
        args = [
            # "--verbose"
        ]
        logging_prefs["driver"] = "ALL"

    options.set_capability("goog:loggingPrefs", logging_prefs)

    if driver_path:
        service = ChromeService(
            executable_path=driver_path,
            service_args=args,
            log_path=logpath,
        )
    else:
        service = ChromeService(
            service_args=args,
            log_path=logpath,
        )

    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.close()


def confirm_data(data):
    assert len(data["inapplicable"]) == 71
    assert len(data["incomplete"]) == 0
    assert len(data["passes"]) == 7
    assert len(data["violations"]) == 9


@pytest.mark.nondestructive
def test_run_axe_sample_page_firefox(firefox_driver):
    """Run axe against sample page and verify JSON output is as expected."""
    data = _perform_axe_run(firefox_driver)

    confirm_data(data)


@pytest.mark.nondestructive
def test_run_axe_sample_page_chrome(chrome_driver):
    """Run axe against sample page and verify JSON output is as expected."""
    data = _perform_axe_run(chrome_driver)

    confirm_data(data)


def _perform_axe_run(driver):
    driver.get("file://" + _DEFAULT_TEST_FILE)
    axe = Axe(driver)
    axe.inject()
    data = axe.run()
    return data


def test_write_results_to_file(tmpdir, mocker):
    axe = Axe(mocker.MagicMock())
    data = {"testKey": "testValue"}
    filename = os.path.join(str(tmpdir), "results.json")

    axe.write_results(data, filename)

    with open(filename) as f:
        actual_file_contents = json.loads(f.read())

    assert data == actual_file_contents


def test_write_results_without_filepath(mocker):
    axe = Axe(mocker.MagicMock())
    data = {"testKey": "testValue"}
    cwd = os.getcwd()
    filename = os.path.join(cwd, "results.json")

    axe.write_results(data, filename)
    with open(filename) as f:
        actual_file_contents = json.loads(f.read())

    assert data == actual_file_contents
    assert os.path.dirname(filename) == cwd
