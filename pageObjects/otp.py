import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.browserutils import BrowserUtils


class otpPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 40)

        # Locators
        self.otp_input = (By.ID, "userOTP")
        self.verify_otp_button = (By.CSS_SELECTOR, "button.loginButton.bg-customBlue")
        self.risk_disclosure_button = (By.XPATH, "//button[@id='notify_message_ok_btn']")

    def get_otp(self, otp_value):
        """Enter OTP, then handle Verify or Risk Disclosure button."""
        print("🔎 Waiting for OTP input field...")
        otp_field = self.wait.until(EC.visibility_of_element_located(self.otp_input))
        otp_field.clear()
        otp_field.send_keys(otp_value)
        time.sleep(1)

        print("🔎 Checking which screen is active...")

        # --- Check if Verify OTP button exists ---
        verify_buttons = self.driver.find_elements(*self.verify_otp_button)
        risk_buttons = self.driver.find_elements(*self.risk_disclosure_button)

        if verify_buttons:
            print("✅ Found 'Verify OTP' button — clicking it.")
            self.driver.execute_script("arguments[0].click();", verify_buttons[0])
            time.sleep(2)
        elif risk_buttons:
            print("ℹ️ Verify OTP already done. Risk Disclosure popup detected.")
        else:
            print("⚠️ No Verify OTP or Risk Disclosure buttons yet — waiting a bit...")
            time.sleep(2)

        # --- Wait for and click the 'I understand' button ---
        try:
            print("🔎 Waiting for 'I understand' button...")
            risk_btn = self.wait.until(EC.element_to_be_clickable(self.risk_disclosure_button))
            self.driver.execute_script("arguments[0].click();", risk_btn)
            print("✅ Clicked 'I understand' successfully.")
        except Exception as e:
            print("ℹ️ No Risk Disclosure popup appeared.", e)

        print("✅ OTP verification flow completed.")
        time.sleep(2)

    def get_login_error(self):
        try:
            return self.driver.find_element(*self.error_msg).text
        except:
            return None
