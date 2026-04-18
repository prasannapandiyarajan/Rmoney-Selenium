import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from utils.browserutils import BrowserUtils
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class ProfilePage(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.profile_tab = (By.XPATH, "//span[@id='head_dropdown_userid']/parent::button")
        self.profile = (By.XPATH, "//*[@id='0_userNavigation']")
        self.general = (By.XPATH, "//button[p[contains(text(), 'General')]]")
        self.security = (By.XPATH, "//button[p[contains(text(), 'Security')]]")
        self.market = (By.XPATH, "//button[p[contains(text(), 'Markets')]]")
        self.version_info = (By.XPATH, "//button[p[contains(text(), 'Version Info')]]")
        self.bo_report = (By.XPATH, "//a[normalize-space()='BO reports']")
        self.reports = (By.XPATH, "//a[normalize-space()='Reports']")
        self.developers = (By.XPATH, "//a[normalize-space()='Developers']")
        self.api_docs = (By.XPATH, "//a[normalize-space()='API Docs']")

        # self.about = (By.XPATH, "//button[p[contains(text(), 'About Us')]]")

    def profile_button(self, test_results, expected="pass"):
        elements = [
            ("funds_tab", self.profile_tab),
            ("profile", self.profile),
            ("general", self.general),
            ("security", self.security),
            ("market", self.market),
            ("version_info", self.version_info),
            # ("about", self.about)/
        ]
        for name, locator in elements:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(locator)
                ).click()
                time.sleep(5)
                status = "pass"
                actual_error = ""

            except Exception as e:
                status = "fail"
                actual_error = "XPath not found or invalid xpath"

            test_results.append({
                "Page": "Profile",
                "Testing_Area": name,
                "expected": expected,
                "actual": f"{name} tab clicked and opened successfully" if status == "pass" else actual_error,
                "status": status
            })

    def profile_toggle(self, test_results, expected="pass"):

        toggle_theme1 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[@id='head_dropdown_userid']/parent::button")))
        toggle_theme1.click()
        time.sleep(4)

        toggle_theme_light = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(@class,'rounded-full')]")))
        toggle_theme_light.click()
        time.sleep(4)

        test_results.append({
            "Page": "Profile",
            "Testing_Area": "Toggle theme button",
            "expected": "Toggle theme button clicked",
            "actual": "Toggle theme button opened successfully",
            "status": "pass"
        })
        toggle_theme_dark = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(@class,'rounded-full')]")))
        toggle_theme_dark.click()
        test_results.append({
            "Page": "Profile",
            "Testing_Area": "Toggle theme button",
            "expected": "Toggle theme button clicked",
            "actual": "Toggle theme button closed successfully",
            "status": "pass"
        })
        time.sleep(4)
        #
        # ticker_tape = WebDriverWait(self.driver, 10).until(
        #     EC.visibility_of_element_located((By.XPATH, "//button[contains(@class,'bg-blue-500')]")))
        # ticker_tape.click()
        # test_results.append({
        #     "Page": "Profile",
        #     "Testing_Area": "Ticker tape button",
        #     "expected": "Ticker tape button clicked",
        #     "actual": "Ticker tape button opened successfully",
        #     "status": "pass"
        # })
        # time.sleep(4)
        # ticker_tape_close = WebDriverWait(self.driver, 10).until(
        #     EC.visibility_of_element_located((By.XPATH,
        #                                       "//button[contains(@class,'rounded-full')]")))
        # ticker_tape_close.click()
        # test_results.append({
        #     "Page": "Profile",
        #     "Testing_Area": "Ticker tape button",
        #     "expected": "Ticker tape button clicked",
        #     "actual": "Ticker tape button closed successfully",
        #     "status": "pass"
        # })
        #
        # time.sleep(2)

        # elements = [
        #     # ("funds_tab", self.profile_tab),
        #     # ("profile", self.profile),
        #     # ("general", self.general),
        #     # ("security", self.security),
        #     # ("market", self.market),
        #     # ("version_info", self.version_info),
        #     # ("about", self.about)
        # ]
        # for name, locator in elements:
        #     try:
        #         WebDriverWait(self.driver, 10).until(
        #             EC.element_to_be_clickable(locator)
        #         ).click()
        #         time.sleep(5)
        #         status = "pass"
        #         actual_error = ""
        #
        #     except Exception as e:
        #         status = "fail"
        #         actual_error = "XPath not found or invalid xpath"
        #
        #     test_results.append({
        #         "Page": "Profile",
        #         "Testing_Area": name,
        #         "expected": expected,
        #         "actual": "clicked successfully" if status == "pass" else actual_error,
        #         "status": status
        #     })

    def bo_reports(self, test_results, expected="pass"):
        elements = [
            ("bo_report", self.bo_report),

        ]
        for name, locator in elements:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(locator)
                ).click()
                time.sleep(5)
                status = "pass"
                actual_error = ""

            except Exception as e:
                status = "fail"
                actual_error = "XPath not found or invalid xpath"

            test_results.append({
                "Page": "Profile",
                "Testing_Area": name,
                "expected": expected,
                "actual": f"{name} tab clicked and opened successfully" if status == "pass" else actual_error,
                "status": status
            })

    def reports_(self, test_results, expected="pass"):
        elements = [
            ("funds_tab", self.profile_tab),
            ("profile", self.profile),
            # ("bo_report", self.bo_report),
            ("reports", self.reports),
            # ("developers", self.developers),
            # ("api_docs", self.api_docs),
        ]
        for name, locator in elements:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(locator)
                ).click()
                time.sleep(5)
                status = "pass"
                actual_error = ""

            except Exception as e:
                status = "fail"
                actual_error = "XPath not found or invalid xpath"

            test_results.append({
                "Page": "Profile",
                "Testing_Area": name,
                "expected": expected,
                "actual": f"{name} tab clicked and opened successfully" if status == "pass" else actual_error,
                "status": status
            })

    def get_login_error(self):
        try:
            return self.driver.find_element(*self.error_msg).text
        except:
            return None
