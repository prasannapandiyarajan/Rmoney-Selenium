import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from utils.browserutils import BrowserUtils
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class HoldingsPage(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.holding_tab = (By.ID, '4_heade_tab')
        self.stocks_tab = (By.XPATH, "//button[.//p[normalize-space()='Stocks']]")
        self.mtf_tab = (By.XPATH, "//button[.//p[normalize-space()='MTF']]")

    def stocks_button(self, test_results, expected="pass"):
        elements = [
            ("holding_tab", self.holding_tab),
            ("stocks_tab", self.stocks_tab),
            ("mtf_tab", self.mtf_tab),
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
                "Page": "Holdings",
                "Testing_Area": name,
                "expected": expected,
                "actual": f"{name} tab clicked successfully" if status == "pass" else actual_error,
                "status": status
            })
        # rows = self.driver.find_elements(By.XPATH, "//tbody/tr")
        rows = self.driver.find_elements(By.XPATH, "//tbody//tr[contains(@id,'_Holdings')]")

        for i, row in enumerate(rows):
            try:
                # re-fetch rows fresh each time (avoid stale element reference)
                rows = self.driver.find_elements(By.XPATH, "//tbody//tr[contains(@id,'_Holdings')]")
                row = rows[i]

                # click row (optional if required)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", row)
                row.click()
                time.sleep(12)

                ActionChains(self.driver).move_to_element(row).perform()

                add_btn = row.find_element(By.XPATH, ".//button[normalize-space()='Add']")
                self.driver.execute_script("arguments[0].click();", add_btn)

                time.sleep(5)
                close_orderwindow = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//div[@class='ml-2 cursor-pointer']//*[name()='svg']")))
                close_orderwindow.click()
                ActionChains(self.driver).move_to_element(row).perform()

                exit_btn = row.find_element(By.XPATH, ".//button[normalize-space()='Exit']")
                self.driver.execute_script("arguments[0].click();", exit_btn)

                time.sleep(5)
                close_orderwindow = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//div[@class='ml-2 cursor-pointer']//*[name()='svg']")))
                close_orderwindow.click()

            except Exception as e:
                print(e)

        # self.driver.find_element(*self.mtf_tab).click()

    # def holdings_list(self):
    #     rows = self.driver.find_elements(By.XPATH, "//tbody/tr")
    #     for i, row in enumerate(rows):
    #         try:
    #             # re-fetch rows fresh each time (avoid stale element reference)
    #             rows = self.driver.find_elements(By.XPATH, "//tbody/tr")
    #             row = rows[i]
    #
    #             # click row (optional if required)
    #             self.driver.execute_script("arguments[0].scrollIntoView(true);", row)
    #             row.click()
    #             time.sleep(12)
    #
    #             ActionChains(self.driver).move_to_element(row).perform()
    #
    #             add_btn = row.find_element(By.XPATH, ".//button[normalize-space()='Add']")
    #             self.driver.execute_script("arguments[0].click();", add_btn)
    #
    #             time.sleep(5)
    #             close_orderwindow = WebDriverWait(self.driver, 10).until(
    #                 EC.visibility_of_element_located(
    #                     (By.XPATH, "//div[@class='ml-2 cursor-pointer']//*[name()='svg']")))
    #             close_orderwindow.click()
    #             ActionChains(self.driver).move_to_element(row).perform()
    #
    #             exit_btn = row.find_element(By.XPATH, ".//button[normalize-space()='Exit']")
    #             self.driver.execute_script("arguments[0].click();", exit_btn)
    #
    #             time.sleep(5)
    #             close_orderwindow = WebDriverWait(self.driver, 10).until(
    #                 EC.visibility_of_element_located(
    #                     (By.XPATH, "//div[@class='ml-2 cursor-pointer']//*[name()='svg']")))
    #             close_orderwindow.click()
    #
    #         except Exception as e:
    #             print(e)
    #
    #     self.driver.find_element(*self.mtf_tab).click()

    def get_login_error(self):
        try:
            return self.driver.find_element(*self.error_msg).text
        except:
            return None
