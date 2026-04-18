import time

from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from utils.browserutils import BrowserUtils
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class predefinedWatchList(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

        # self.setting_icon = (By.XPATH, "//button[contains(@class,'popover-button')]")
        # self.sorting_tab = (By.XPATH, "//button[.//p[text()='Sorting']]")
        # self.small_button = (By.XPATH, "//button[normalize-space()='S']")
        # self.large_button = (By.XPATH, "//button[normalize-space()='M']")
        # self.medium_button = (By.XPATH, "//button[normalize-space()='L']")
        # self.xtra_large_button = (By.XPATH, "//button[normalize-space()='XL']")
        # self.sort_by_atoz = (By.XPATH, "//button[normalize-space()='A-Z']")
        # self.sort_by_percentage = (By.XPATH, "//button[normalize-space()='(%)']")
        # self.sort_by_ltp = (By.XPATH, "//button[normalize-space()='LTP']")
        # self.sort_by_exec = (By.XPATH, "//button[normalize-space()='Exc']")
        # self.exch_nfo = (By.XPATH, "//button[normalize-space()='NFO']")
        # self.exch_bse = (By.XPATH, "//button[normalize-space()='BSE']")
        # self.exch_cds = (By.XPATH, "//button[normalize-space()='CDS']")
        # self.exch_mcx = (By.XPATH, "//button[normalize-space()='MCX']")
        # self.exch_nse = (By.XPATH, "//button[normalize-space()='NSE']")
        # self.preference_tab = (By.XPATH, "//button[.//p[normalize-space(text())='Preference']]")
        # self.basic = (By.XPATH, "//button[text()='Basic']")
        # self.depth = (By.XPATH, "//button[text()='Depth")
        # self.all = (By.XPATH, "//button[text()='All']")
        # self.top = (By.XPATH, "//button[text()='Top']")
        # self.bottom = (By.XPATH, "//button[text()='Bottom']")
        # self.open = (By.XPATH, "//button[text()='Open']")
        # self.close = (By.XPATH, "//button[text()='Close']")
        # self.research_ideas = (By.ID, "Research-Ideas")
        # self.setting_tab = (By.XPATH, "//button[.//p[normalize-space(text())='Settings']]")
        # self.edit_watchlist = (By.CSS_SELECTOR,
        #                        "section section section:nth-child(1) div:nth-child(1) div:nth-child(2) div:nth-child(2) figure:nth-child(1) svg")
        self.predefined_tab = (By.XPATH, "//section[normalize-space()='Predefined list']")
        self.nifty_tab = (By.ID, "watchlisttab0]")
        self.banknifty_tab = (By.ID, "watchlisttab1")
        self.sensex_tab = (By.ID, "watchlisttab2]")
        self.rmoney_tab = (By.ID, "watchlisttab3")
        self.holdings_tab = (By.ID, "watchlisttab4")


    def predefined_watchlist_tab(self, test_results, expected="pass"):
        elements = [
            ("predefined_tab", self.predefined_tab),
            ("nifty_tab", self.nifty_tab),
            ("banknifty_tab", self.banknifty_tab),
            ("sensex_tab", self.sensex_tab),
            ("rmoney_tab", self.rmoney_tab),
            ("holdings_tab", self.holdings_tab),
            # ("sorting_tab", self.sorting_tab),
            # ("small_button", self.small_button),
            # ("large_button", self.large_button),
            # ("medium_button", self.medium_button),
            # ("xtra_large_button", self.xtra_large_button),
            # ("sort_by_atoz", self.sort_by_atoz),
            # ("sort_by_percentage", self.sort_by_percentage),
            # ("sort_by_ltp", self.sort_by_ltp),
            # ("exch_nfo", self.exch_nfo),
            # ("exch_bse", self.exch_bse),
            # ("exch_cds", self.exch_cds),
            # ("exch_mcx", self.exch_mcx),
            # ("exch_nse", self.exch_nse),
            # ("preference_tab", self.preference_tab),
            # ("basic", self.basic),
            # ("depth", self.depth),
            # ("all", self.all),
            # ("top", self.top),
            # ("bottom", self.bottom),
            # ("open", self.open),
            # ("close", self.close),
            # ("research_ideas", self.research_ideas),
            # ("setting_tab", self.setting_tab),
            # ("edit_watchlist", self.edit_watchlist),
            # ("input_field", self.input_field),


            # add more buttons if needed
        ]

        for name, locator in elements:
            try:
                element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(locator)
                ).click()
                time.sleep(5)
                if name == 'input_field':
                    input_field = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located(
                            (By.ID, "rename_inp")
                        )
                    )
                    # Clear and type new name
                    input_field.clear()
                    input_field.send_keys("test1")  # Replace with your desired text
                    time.sleep(2)
                    save_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((
                            By.CSS_SELECTOR,
                            "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > section:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > section:nth-child(4) > div:nth-child(1) > section:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > figure:nth-child(2) > svg:nth-child(1) > path:nth-child(1)"
                        ))
                    )

                    # Click the save button
                    save_button.click()
                status = "pass"
                actual_error = ""

            except Exception as e:
                status = "fail"
                actual_error = "XPath not found or invalid xpath"

            test_results.append({
                "watchlist_bottom_tab": name,
                "expected": expected,
                "actual": f"{name} button clicked successfully" if status == "pass" else actual_error,
                "status": status
            })

            time.sleep(2)

        status = "pass"
        actual_error = ""





    def get_login_error(self):
        try:
            return self.driver.find_element(*self.error_msg).text
        except:
            return None
