import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from utils.browserutils import BrowserUtils
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class FundsPage(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.funds_tab = (By.ID, '5_heade_tab')
        self.add_withdrawal_fund = (By.XPATH, "//button[normalize-space()='Withdraw']")
        self.funds_available = (
            By.XPATH, "//div[normalize-space()='Funds Available']")
        self.add_funds = (
            By.XPATH,
            "//button[@class='w-full md:w-[6rem] h-[2rem] owPositiveBackground font-medium text-sm text-white rounded-[.25rem]']")
        self.funds_cancel = (By.ID, "deposite_cancel")

    def funds_button(self, test_results, expected="pass"):
        elements = [
            ("funds_tab", self.funds_tab),
            # ("add_withdrawal_fund", self.add_withdrawal_fund),
            # ("funds_available", self.funds_available),
            ("collateral_available", self.add_funds),
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
                "Page": "Funds",
                "Testing_Area": name,
                "expected": expected,
                "actual": f"{name} tab clicked successfully" if status == "pass" else actual_error,
                "status": status
            })
        funds_amount = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter amount (Min 50)']"))
        )
        funds_amount.click()
        funds_amount.send_keys("100")
        time.sleep(5)
        funds_amount.clear()
        test_results.append({
            "Page": "Funds",
            "Testing_Area": "Amount field",
            "expected": "Amount field clicked",
            "actual": "Amount field clicked and pass value successfully",
            "status": "pass"
        })
        time.sleep(2)
        upi_id = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Eg: USERNAME@upi']"))
        )
        upi_id.click()
        upi_id.send_keys("sm@upi")
        time.sleep(5)
        upi_id.clear()
        test_results.append({
            "Page": "Funds",
            "Testing_Area": "UPI field",
            "expected": "UPI field clicked",
            "actual": "UPI field clicked and pass value successfully",
            "status": "pass"
        })
        time.sleep(5)
        submit = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.ID, "deposite_proceed"))
        )
        submit.click()
        time.sleep(5)
        test_results.append({
            "Page": "Funds",
            "Testing_Area": "Submit button",
            "expected": "Submit button",
            "actual": "Submit button clicked successfully",
            "status": "pass"
        })
        time.sleep(5)
        cancel = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.ID, "deposite_cancel"))
        )
        cancel.click()
        time.sleep(5)
        test_results.append({
            "Page": "Funds",
            "Testing_Area": "Cancel button",
            "expected": "Cancel button",
            "actual": "Cancel button clicked successfully",
            "status": "pass"
        })
        withdraw_button = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Withdraw']]"))
        )
        withdraw_button.click()
        test_results.append({
            "Page": "Funds",
            "Testing_Area": "Withdraw button",
            "expected": "Withdraw button",
            "actual": "Withdraw button clicked successfully",
            "status": "pass"
        })

        withdraw_amount = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='₹ Enter Amount']"))
        )
        withdraw_amount.click()
        withdraw_amount.send_keys("100")
        test_results.append({
            "Page": "Funds",
            "Testing_Area": "Withdraw Amount field",
            "expected": "Withdraw Amount field clicked",
            "actual": "Withdraw Amount field clicked and pass value successfully",
            "status": "pass"
        })
        time.sleep(2)
        withdraw_btn = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//p[normalize-space()='Withdraw']]"))
        )
        withdraw_btn.click()
        time.sleep(5)
        test_results.append({
            "Page": "Funds",
            "Testing_Area": "Withdraw button",
            "expected": "Withdraw button",
            "actual": "Withdraw button clicked successfully",
            "status": "pass"
        })
        time.sleep(5)
        with_draw_cancel = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Cancel']"))
        )
        with_draw_cancel.click()
        time.sleep(5)
        test_results.append({
            "Page": "Funds",
            "Testing_Area": "Withdraw Cancel button",
            "expected": "Withdraw Cancel button",
            "actual": "Withdraw Cancel button clicked successfully",
            "status": "pass"
        })

    def get_login_error(self):
        try:
            return self.driver.find_element(*self.error_msg).text
        except:
            return None
