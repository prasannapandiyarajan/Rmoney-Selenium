import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from utils.browserutils import BrowserUtils
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class MutualFundPage(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.mutual_fund_tab = (By.XPATH, "//button[.//p[normalize-space()='Mutual Funds']]")
        self.discover_tab = (By.XPATH, "//button[.//p[normalize-space()='Discover']]")
        self.portfolio_tab = (By.XPATH, "//button[.//p[normalize-space()='Portfolio']]")
        self.order_tab = (By.XPATH, "//button[.//p[normalize-space()='Orders']]")
        self.onetime_tab = (By.XPATH, "//ul[@id='header_tab_list']//button[.//p[normalize-space()='One Time']]")
        self.sip_tab = (By.XPATH, "//ul[@id='header_tab_list']//button[.//p[normalize-space()='SIP']]")
        self.mandate_tab = (By.XPATH, "//button[.//p[normalize-space()='Mandate']]")
        self.redeem_tab = (By.XPATH, "//ul[@id='header_tab_list']//button[.//p[normalize-space()='Redeem']]")
        self.cancel_tab = (By.XPATH, "//ul[@id='header_tab_list']//button[.//p[normalize-space()='Cancel']]")
        self.watchlist_tab = (By.XPATH, "//button[.//p[normalize-space()='Watchlist']]")
        # self.products_tab = (By.ID, "Products")
        # self.mutual_funds_tab = (By.ID, "0_explore_activeTab")
        # self.ipo_tab = (By.ID, "1_explore_activeTab")
        # self.global_investing_tab = (By.ID, "2_explore_activeTab")
        # self.tax_filling_tab = (By.ID, "3_explore_activeTab")
        # self.nps_online_tab = (By.ID, "4_explore_activeTab")
        # self.grobox_tab = (By.ID, "5_explore_activeTab")
        # self.smallcase_tab = (By.ID, "6_explore_activeTab")
        # self.tradebox_tab = (By.ID, "7_explore_activeTab")
        # self.instaoptions_tab = (By.ID, "8_explore_activeTab")
        # self.more_tab = (By.ID, "More")
        # self.form_format_tab = (By.ID, "0_explore_activeTab")
        # self.offer_to_tab = (By.ID, "1_explore_activeTab")
        # self.offer_for_sale_tab = (By.ID, "2_explore_activeTab")

    def mutual_fund_page(self, test_results, expected="pass"):
        elements = [
            ("mutual_fund_tab", self.mutual_fund_tab),
            ("discover_tab", self.discover_tab),
            ("portfolio_tab", self.portfolio_tab),
            ("order_tab", self.order_tab),
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
                "Page": "Mutual Fund",
                "Testing_Area": name,
                "expected": expected,
                "actual": "clicked successfully" if status == "pass" else actual_error,
                "status": status
            })

    def mutual_fund_orders(self, test_results, expected="pass"):
        elements = [
            ("onetime_tab", self.onetime_tab),
            ("sip_tab", self.sip_tab),
            ("mandate_tab", self.mandate_tab),
            ("reedem_tab", self.redeem_tab),
            ("cancel_tab", self.cancel_tab),
        ]
        for names, locator2 in elements:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(locator2)
                ).click()
                time.sleep(5)
                status = "pass"
                actual_error = ""

            except Exception as e:
                status = "fail"
                actual_error = "XPath not found or invalid xpath"

            test_results.append({
                "Page": "Mutual Fund",
                "Testing_Area": names,
                "expected": expected,
                "actual": "clicked successfully" if status == "pass" else actual_error,
                "status": status
            })

    def mutual_fund_watchlist(self, test_results, expected="pass"):
        elements = [
            ("watchlist_tab", self.watchlist_tab),
        ]
        for names, locator2 in elements:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(locator2)
                ).click()
                time.sleep(1)
                status = "pass"
                actual_error = ""

            except Exception as e:
                status = "fail"
                actual_error = "XPath not found or invalid xpath"

            test_results.append({
                "Page": "Mutual Fund",
                "Testing_Area": names,
                "expected": expected,
                "actual": "clicked successfully" if status == "pass" else actual_error,
                "status": status
            })

    def get_login_error(self):
        try:
            return self.driver.find_element(*self.error_msg).text
        except:
            return None
