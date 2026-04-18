import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from utils.browserutils import BrowserUtils
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class WatchList(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.search_scrip_input = (By.ID, 'watch_search_inp')

        # self.predefined_tab = (By.ID, "mw_Predefined List_tab")
        # self.my_stock_button = (By.XPATH, "//a[span[text()='MY STOCKS']]")
        # self.nifty_stock = (By.XPATH, "//a[span[text()='NIFTY 5000']]")
        self.setting_icon = (By.XPATH, "//div[contains(@class,'border-primary') and contains(@class,'rounded')]")
        self.sorting_tabs = (By.XPATH,"//button[.//p[normalize-space()='Sorting']]")
        self.sort_scrips = (By.XPATH, "//button[normalize-space()='A-Z']")
        self.percentage = (By.XPATH, "//button[normalize-space()='(%)']")
        self.ltp_button = (By.XPATH, "//button[normalize-space()='LTP']")
        self.exec_button = (By.XPATH, "//button[normalize-space()='Exc']")
        self.ncx_button = (By.XPATH, "//button[normalize-space()='NCX']")
        self.nfo_button = (By.XPATH, "//button[normalize-space()='NFO']")
        self.mcx_button = (By.XPATH, "//button[normalize-space()='MCX']")
        self.nse_button = (By.XPATH, "//button[normalize-space()='NSE']")
        self.preference_button = (By.ID, "Preference_btn")
        self.small_button = (By.XPATH, "//button[normalize-space()='S']")
        self.medium_button = (By.XPATH, "//button[normalize-space()='M']")
        self.large_button = (By.XPATH, "//button[normalize-space()='L']")
        self.xtra_large_button = (By.XPATH, "//button[normalize-space()='XL']")
        self.basic_button = (By.XPATH, "//button[normalize-space()='Basic']")
        # self.basic_radio_box = (By.ID, "basic")
        self.depth_button = (By.XPATH, "//button[normalize-space()='Depth']")
        self.all_button = (By.XPATH, "//button[normalize-space()='All']")
        self.top_button = (By.XPATH, "//button[normalize-space()='Top']")
        self.bottom_button = (By.XPATH, "//button[normalize-space()='Bottom']")
        self.open_button = (By.XPATH, "//button[normalize-space()='Open']")
        self.close_button = (By.XPATH, "//button[normalize-space()='Close']")
        self.edit_button = (By.XPATH, "Edit_btn")
        self.cursor_button = (By.CSS_SELECTOR,
                              "body > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > a:nth-child(3) > svg:nth-child(1)")
        self.cursor_button_2 = (By.CSS_SELECTOR,
                                "body > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > a:nth-child(3) > svg:nth-child(1)")
        self.cursor_button_3 = (By.CSS_SELECTOR,
                                "body > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(3) > div:nth-child(3) > div:nth-child(2) > a:nth-child(3) > svg:nth-child(1)")
        self.cursor_button_4 = (By.CSS_SELECTOR,
                                "body > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(3) > div:nth-child(4) > div:nth-child(2) > a:nth-child(3) > svg:nth-child(1)")
        self.cursor_button_5 = (By.CSS_SELECTOR,
                                "body > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(5) > div:nth-child(2) > a:nth-child(3) > svg:nth-child(1)")

        # self.close_button = (By.CSS_SELECTOR,
        #                      "button[class='size-8 bg-[#0d45930f] text-center primaryColor mr-2 cursor-pointer flex justify-center items-center rounded']")
        self.add_scrips = (By.CSS_SELECTOR,
                           "button[class='size-8 bg-[#44b748] border-[#44b748] flex justify-center items-center rounded text-center text-white cursor-pointer']")

        self.watchlist_input_field = (By.ID, "renameInp_0")
        self.watchlist_input_field_2 = (By.ID, "renameInp_1")
        self.watchlist_tab = (By.XPATH, "//section[normalize-space()='Watchlist']")
        self.preference_tab = (By.XPATH, "//button[.//p[normalize-space(text())='Preference']]")
        self.setting_tab = (By.XPATH, "//button[.//p[normalize-space(text())='Settings']]")
        self.edit_watchlist = (By.CSS_SELECTOR,
                               "section section section:nth-child(1) div:nth-child(1) div:nth-child(2) div:nth-child(2) figure:nth-child(1) svg")
        self.input_field = (By.ID, "rename_inp")
        # self.watchlist_input_field_3 = (By.ID, "renameInp_2")
        # self.watchlist_input_field_4 = (By.ID, "renameInp_3")
        # self.watchlist_input_field_5 = (By.ID, "renameInp_4")

    def watchlist_setting(self, test_results, expected="pass"):

        elements = [
            ("watchlist_tab", self.watchlist_tab),
            ("setting_icon", self.setting_icon),
            ("small_button", self.small_button),
            ("medium_button", self.medium_button),
            ("large_button", self.large_button),
            ("xtra_large_button", self.xtra_large_button),
            ("sort_scrips", self.sort_scrips),
            ("percentage", self.percentage),
            ("ltp_button", self.ltp_button),
            ("exec_button", self.exec_button),
            ("ncx_button", self.ncx_button),
            ("nfo_button", self.nfo_button),
            ("mcx_button", self.mcx_button),
            ("nse_button", self.nse_button),
            ("preference_tab", self.preference_tab),
            ("basic_button", self.basic_button),
            ("depth_button", self.depth_button),
            ("all_button", self.all_button),
            ("top_button", self.top_button),
            ("bottom_button", self.bottom_button),
            ("open_button", self.open_button),
            ("close_button", self.close_button),
            ("setting_tab", self.setting_tab),
            ("edit_watchlist", self.edit_watchlist),
            ("input_field", self.input_field),
        ]

        # ----------------------------
        # Step 1: Click Watchlist Settings Options
        # ----------------------------
        for name, locator in elements:
            status = "pass"
            actual_error = ""

            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(locator)
                ).click()

            except Exception as e:
                status = "fail"
                actual_error = f"Click failed: {str(e)}"

            test_results.append({
                "watchlist_bottom_tab": name,
                "expected": expected,
                "actual": "Clicked successfully" if status == "pass" else actual_error,
                "status": status
            })
        save_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='submit' and contains(@class,'bg-[#44b748]')]")
            )
        )
        save_button.click()

        # ----------------------------
        # Step 2: Rename Watchlists
        # ----------------------------
        # new_names = ["Watchlist1", "Watchlist2", "Watchlist3", "Watchlist4", "Watchlist5"]
        #
        # status = "pass"
        # actual_error = ""
        #
        # try:
        #     for idx, new_name in enumerate(new_names):
        #         # Always fetch edit button fresh (avoid stale element issue)
        #         edit_button = WebDriverWait(self.driver, 10).until(
        #             EC.element_to_be_clickable(
        #                 (By.XPATH, f"(//a//*[name()='svg'][contains(@class,'cursor-pointer')])[{idx + 1}]")
        #             )
        #         )
        #         edit_button.click()
        #
        #         # Wait for the input field to appear for this row
        #         input_field = WebDriverWait(self.driver, 10).until(
        #             EC.visibility_of_element_located(
        #                 (By.XPATH, f"//input[contains(@id,'renameInp_')]")
        #             )
        #         )
        #
        #         # Clear and type new name
        #         input_field.clear()
        #         input_field.send_keys(new_name)
        #
        #         # Click the ✔ save button for this row
        #         save_button = WebDriverWait(self.driver, 10).until(
        #             EC.element_to_be_clickable(
        #                 (By.XPATH, "//button[@type='submit' and contains(@class,'bg-[#44b748]')]")
        #             )
        #         )
        #         save_button.click()
        #
        #         # Small wait for DOM to stabilize before next loop
        #         time.sleep(1)
        #     actual_error = "Renamed all watchlists successfully"
        #
        # except Exception as e:
        #     status = "fail"
        #     actual_error = str(e)
        #
        # test_results.append({
        #     "watchlist_bottom_tab": "watchlist rename",
        #     "expected": "All 5 lists renamed",
        #     "actual": actual_error,
        #     "status": status
        # })
        # Step 2: Rename Watchlists

    def get_login_error(self):
        try:
            return self.driver.find_element(*self.error_msg).text
        except:
            return None
