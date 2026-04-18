import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from utils.browserutils import BrowserUtils
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class PositionPage(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.position_tab = (By.ID, '3_heade_tab')
        self.all_tab = (By.XPATH, "//button[p[contains(text(), 'All')]]")
        self.equity_tab = (By.XPATH, "//button[p[contains(text(), 'Equity')]]")
        self.fno_tab = (By.XPATH, "//button[.//p[normalize-space()='F&O']]")
        self.commodity_tab = (By.XPATH, "//button[.//p[normalize-space()='MCX']]")
        self.currency_tab = (By.XPATH, "//button[.//p[normalize-space()='Currency']]")

    def position_button(self, test_results, expected="pass"):
        elements = [
            ("position_tab", self.position_tab),
            ("all_tab", self.all_tab),
            ("equity_tab", self.equity_tab),
            ("fno_tab", self.fno_tab),
            ("commodity_tab", self.commodity_tab),
            ("currency_tab", self.currency_tab),
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
                "Page": "Position",
                "Testing_Area": name,
                "expected": expected,
                "actual": f"{name} tab clicked successfully" if status == "pass" else actual_error,
                "status": status
            })

    def position_list(self, test_results, expected="pass"):
        driver = self.driver
        wait = WebDriverWait(driver, 12)
        actions = ActionChains(driver)
        action_log = []
        # test_results = []
        # more_logged = False
        # info_logged = False
        # history_logged = False
        equity_tab = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[p[contains(text(), 'Equity')]]")
            )
        )
        equity_tab.click()
        rows = driver.find_elements(By.XPATH, "//tbody/tr")

        for i, row in enumerate(rows):
            try:
                # re-fetch rows fresh each time (avoid stale element reference)
                rows = driver.find_elements(By.XPATH, "//tbody/tr")
                row = rows[i]

                # click row (optional if required)
                driver.execute_script("arguments[0].scrollIntoView(true);", row)
                row.click()

                add_btn = row.find_element(By.XPATH, "//button[normalize-space()='Add']")
                driver.execute_script("arguments[0].click();", add_btn)
                time.sleep(5)

                wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//div[@class='ml-2 cursor-pointer']//*[name()='svg']"))).click()

                test_results.append({
                    "Page": "Position",
                    "Testing_Area": "Click Add button",
                    "expected": expected,
                    "actual": "Click Add button opened order-window and closed successfully ",
                    "status": "Pass"
                })
                time.sleep(5)

                # close_btn = row.find_element(By.XPATH, "//div[@class='ml-2 cursor-pointer']//*[name()='svg']")
                # driver.execute_script("arguments[0].click();", close_btn)
                #
                # time.sleep(5)
                row.click()
                exit_btn = row.find_element(By.XPATH, "//button[normalize-space()='Exit']")
                driver.execute_script("arguments[0].click();", exit_btn)

                wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//div[@class='ml-2 cursor-pointer']//*[name()='svg']"))).click()

                test_results.append({
                    "Page": "Position",
                    "Testing_Area": "Click Exit button",
                    "expected": expected,
                    "actual": "Click Exit button opened order-window and closed successfully ",
                    "status": "Pass"
                })
                time.sleep(5)

                row.click()
                more_btn = row.find_element(By.XPATH, "//button[normalize-space()='More']")
                driver.execute_script("arguments[0].click();", more_btn)
                time.sleep(5)
                info_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//span[normalize-space()='Info']/ancestor::button")))
                info_button.click()

                time.sleep(5)

                close_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[normalize-space()='Close']")))
                close_button.click()

                row.click()
                more_btn = row.find_element(By.XPATH, "//button[normalize-space()='More']")
                driver.execute_script("arguments[0].click();", more_btn)
                time.sleep(5)

                convert_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//span[normalize-space()='Convert']/ancestor::button")))
                convert_button.click()
                time.sleep(5)

                close_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[normalize-space()='Close']")))
                close_button.click()


                # time.sleep(5)
                # close_btn = row.find_element(By.XPATH, "//div[@class='ml-2 cursor-pointer']//*[name()='svg']")
                # driver.execute_script("arguments[0].click();", close_btn)
                #
                # time.sleep(5)

                # more_btn = row.find_element(By.XPATH, ".//button[contains(@id,'opt_btn')]")
                # driver.execute_script("arguments[0].click();", more_btn)
                #
                # time.sleep(5)

                # if not more_logged:
                #     test_results.append({
                #         "Page": "Order Book",
                #         "Testing_Area": "More button",
                #         "expected": "More button clicked",
                #         "actual": "More button clicked of show info option button",
                #         "status": "pass"
                #     })
                #     more_logged = True

                # wait and click Info in the dropdown
                # info_option = WebDriverWait(driver, 5).until(
                #     EC.element_to_be_clickable((By.XPATH, "//div[@role='menu']//div[normalize-space()='Info']"))
                # )
                # info_option.click()
                # if not info_logged:
                #     test_results.append({
                #         "Page": "Order Book",
                #         "Testing_Area": "Info button",
                #         "expected": "Info button clicked",
                #         "actual": "Info button clicked and scrip-details info opened successfully",
                #         "status": "pass"
                #     })
                #     time.sleep(2)
                #     info_logged = True
                #
                # information_tab = WebDriverWait(driver, 5).until(
                #     EC.element_to_be_clickable((By.XPATH, "//button[@id='Information']"))
                # )
                # information_tab.click()
                # #
                # history_tab = WebDriverWait(driver, 5).until(
                #     EC.element_to_be_clickable((By.XPATH,
                #                                 "//button[@id='History']"))
                # )
                # history_tab.click()
                # if not history_logged:
                #     test_results.append({
                #         "Page": "Order Book",
                #         "Testing_Area": "History button",
                #         "expected": "History button clicked",
                #         "actual": "History button clicked and order-details opened successfully",
                #         "status": "pass"
                #     })
                #
                #     history_logged = True
                #
                # cancel_button = WebDriverWait(driver, 5).until(
                #     EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Close']"))
                # )
                # cancel_button.click()
                # time.sleep(3)

            except Exception as e:
                print(e)
                # driver.execute_script("arguments[0].click();", more_btn)

                # wait and click Info in the dropdown
                # info_option = WebDriverWait(driver, 5).until(
                #     EC.element_to_be_clickable((By.XPATH, "//div[@role='menu']//div[normalize-space()='Info']"))
                # )
                # info_option.click()
                time.sleep(2)

                # information_tab = WebDriverWait(driver, 5).until(
                #     EC.element_to_be_clickable((By.XPATH, "// button[span[normalize - space() = 'Information']]"))
                # )
                # information_tab.click()
    def get_login_error(self):
        try:
            return self.driver.find_element(*self.error_msg).text
        except:
            return None
