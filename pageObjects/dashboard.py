import time

from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from utils.browserutils import BrowserUtils
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class DashboardPage(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.home_tab = (By.ID, '1_heade_tab')
        # self.equities = (By.ID, 'Equities')
        self.etf = (By.ID, 'ETFs')
        self.ipo = (By.ID, 'IPO')
        self.screeners = (By.ID, 'Screeners')
        self.it_sector = (By.XPATH, "//button[@id='0_heade_tab']")
        self.auto_sector = (By.XPATH, "//ul[@id='header_tab_list']//button[p[normalize-space()='AUTOMOBILE']]")
        self.telecom_sector = (By.XPATH, "//ul[@id='header_tab_list']//button[p[normalize-space()='TELECOM']]")
        self.pharma_sector = (By.XPATH, "//ul[@id='header_tab_list']//button[p[normalize-space()='PHARMA']]")
        self.healthcare_sector = (By.XPATH, "//ul[@id='header_tab_list']//button[p[normalize-space()='HEALTHCARE']]")
        self.banking_sector = (By.XPATH, "//ul[@id='header_tab_list']//button[p[normalize-space()='BANKING']]")
        self.energy_sector = (By.XPATH, "//ul[@id='header_tab_list']//button[p[normalize-space()='ENERGY']]")
        self.fmcg_sector = (By.XPATH, "//ul[@id='header_tab_list']//button[p[normalize-space()='FMCG']]")
        self.finance_sector = (By.XPATH, "//ul[@id='header_tab_list']//button[p[normalize-space()='FINANCIALS']]")
        self.index = (By.XPATH, "//ul[@id='header_tab_list']//button[p[normalize-space()='INDEX BASED']]")
        self.equity = (By.XPATH, "//ul[@id='header_tab_list']//button[p[normalize-space()='Equity']]")
        self.sector = (By.XPATH, "//ul[@id='header_tab_list']//button[p[normalize-space()='Sector']]")
        self.gold = (By.XPATH, "//ul[@id='header_tab_list']//button[p[normalize-space()='Gold']]")
        self.debt = (By.XPATH, "//ul[@id='header_tab_list']//button[p[normalize-space()='Debt']]")
        self.global_ = (By.XPATH, "//ul[@id='header_tab_list']//button[p[normalize-space()='Global']]")
        self.ongoing = (By.XPATH, "//ul[@id='header_tab_list']//button[p[normalize-space()='Ongoing']]")
        self.ipo_applied = (By.XPATH, "//ul[@id='header_tab_list']//button[p[normalize-space()='IPO Applied']]")
        self.recently_listed = (By.XPATH, "//ul[@id='header_tab_list']//button[p[normalize-space()='Recently Listed']]")
        self.announced = (By.XPATH, "//ul[@id='header_tab_list']//button[p[normalize-space()='Announced']]")
        self.top_gainer = (By.XPATH, "//ul[@id='header_tab_list']//button[p[normalize-space()='Top Gainers']]")
        self.top_looser = (By.XPATH, "//ul[@id='header_tab_list']//button[p[normalize-space()='Top Losers']]")
        self.week_high = (By.XPATH, "//ul[@id='header_tab_list']//button[p[normalize-space()='52 Week High']]")
        self.week_low = (By.XPATH, "//ul[@id='header_tab_list']//button[p[normalize-space()='52 Week Low']]")
        self.rider = (By.XPATH, "//ul[@id='header_tab_list']//button[p[normalize-space()='Riders']]")
        self.dragger = (By.XPATH, "//ul[@id='header_tab_list']//button[p[normalize-space()='Draggers']]")
        self.top_volume = (By.XPATH, "//ul[@id='header_tab_list']//button[p[normalize-space()='Top Volume']]")
        self.payin_button = (By.XPATH, "//button[@id='payIn_nav']")
        self.home_path = (By.XPATH, "//p[normalize-space()='Home']")
        self.holdings_path = (By.XPATH, "//*[@id='portfolio_view']")
        self.individual_value = (By.XPATH, "//input[@id='Current value']")
        self.investment_value = (By.XPATH, "//input[@id='Investment value']")
        self.pnl_value = (By.XPATH, "//input[@id='P&L']")
        self.option_chain_snapAlpha = (
            By.XPATH, "//div[contains(@class,'relative') and .//div[normalize-space()='Option Chain']]")
        self.scalper_snapAlpha = (By.XPATH, "//div[.//div[normalize-space()='Scalper']]")
        self.research_ideas_viewAll = (
            By.XPATH, "//div[contains(@class,'profileDp') and .//span[normalize-space()='View All']]")
        self.intraday_sub_tab = (By.XPATH, "//a[@aria-current='page' and normalize-space()='Intraday']")
        self.delivery_sub_tab = (By.XPATH, "//a[normalize-space()='Delivery']")
        self.commodity_tab = (By.XPATH, "//button[.//p[normalize-space()='Commodity']]")
        self.basket_button = (By.XPATH, "//button[.//p[normalize-space()='Stock Basket']]")
        self.invest_button = (By.XPATH, "//button[normalize-space()='Invest']")
        self.back_button = (By.XPATH, "//div[contains(@class,'cursor-pointer') and contains(@class,'size-[24px]')]")
        self.basket_FNO_button = (By.XPATH, "//button[.//p[normalize-space()='Basket FNO']]")
        self.back_button_ = (By.XPATH, "'//figure[@class='cursor-pointer']//span//*[name()='svg']'")
        # self.todays_pnl = (By.ID, 'todays_pnl')
        # self.home_funds_label = (By.ID, 'home_funds_label')
        # self.ava_label = (By.ID, 'ava_label')
        # self.margin_used_label = (By.ID, 'margin_used_label')
        # self.open_bal_label = (By.ID, 'open_bal_label')
        # self.payIn_nav = (By.ID, 'payIn_nav')
        # self.grobox_iifl = (By.ID, 'smallCases_head')
        # self.insta_options = (By.ID, 'smallCases_head')
        # self.invest_stock_label = (By.ID, 'invest_stock_label')
        # self.equities_ideas = (By.ID, 'Equity Ideas')
        # self.equit_tab = (By.XPATH, "//nav[@id='tab_navbar']//a[@id='Equity']")
        # self.equities_ideas = (By.XPATH, "//div[@id='Equity Ideas' and contains(@class, 'cursor-pointer')]")
        # self.long_term = (By.XPATH, "//button[span[text()='Long Term']]")
        # self.short_term = (By.XPATH, "//button[span[text()='Short Term']]")
        # self.intraday = (By.XPATH, "//button[span[text()='Intraday']]")
        # self.drop_down = (By.XPATH, "//button[.//span[text()='All Calls']]")
        # self.all_calls = (By.XPATH, "//ul[@role='listbox']//li[.//span[text()='All Calls']]")
        # self.open_calls = (By.XPATH, "//ul[@role='listbox']//li[.//span[text()='Open Calls']]")
        # self.closed_all = (By.XPATH, "//ul[@role='listbox']//li[.//span[text()='Closed Calls']]")
        # self.all_tab = (By.XPATH, "//button[span[text()='All']]")
        # self.buy_tab = (By.XPATH, "//button[span[text()='Buy']]")
        # self.sell_tab = (By.XPATH, "//button[span[text()='Sell']]")
        # self.fno_tab = (By.ID, "F&O")
        # self.commodity_tab = (By.ID, 'Commodity')
        # self.order_tab = (By.ID, "2_heade_tab")
        # self.all_order = (By.XPATH, "//nav[@id='tab_navbar']//a[contains(text(), 'All')]")
        # self.pending_order = (By.XPATH, "//nav[@id='tab_navbar']//a[contains(text(), 'Pending')]")
        # self.executed_order = (By.XPATH, "//nav[@id='tab_navbar']//a[contains(text(), 'Executed')]")
        # self.gtt_order = (By.XPATH, "//nav[@id='tab_navbar']//a[contains(text(), 'GTT')]")
        # self.refresh_button = (By.XPATH, "//button[contains(text(), 'Refresh') and contains(@class, 'outlined_btn')]")
        # self.position_tab = (By.ID, "3_heade_tab")
        # self.holdings_tab = (By.ID, "4_heade_tab")
        # self.funds_tab = (By.ID, "5_heade_tab")
        # self.investment_label = (By.ID, "investment_label")
        # self.current_value = (By.ID, "Current_value")
        # self.profit_loss = (By.ID, "profit_loss")
        # self.add_withdrawal_fund = (By.XPATH, "//button[contains(text(), 'Add/Withdraw Funds')]")
        # self.funds_available = (
        # By.XPATH, "//button[@type='button' and @class='cursor-pointer']/img[@alt='downExpandArrow']/parent::button")
        # self.collateral_available = (
        # By.XPATH, "//button[@type='button' and @class='cursor-pointer'][.//img[@alt='downExpandArrow']]")
        # self.explore_tab = (By.ID, "6_heade_tab")
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
        # self.header_menu = (By.ID, "header_menu")
        # self.profile = (By.XPATH,"//a[@role='option' and span[text()='Profile']]")
        # self.reports = (By.XPATH,"//a[@role='option' and .//span[text()='Reports']]")
        # self.settings = (By.XPATH, "//a[span[text()='Settings']]")
        # self.checkbox_orderbook = (By.XPATH, "//tr[td//div[text()='IDEA-EQ']]//input[@type='checkbox']")
        # self.orderbook_modify = (By.XPATH, "//tr[td//div[text()='IDEA-EQ']]//button[contains(text(), 'Modify')]")

        # self.need_help = (By.XPATH, "//a[@role='option' and .//span[text()='Help']]")
        # self.sign_out = (By.XPATH, "//a[@role='option' and .//span[text()='Sign out']]")

        # self.commodity_tab = (By.ID, "Commodity")

    def equity_button(self, test_results, expected="pass"):
        elements = [
            ("home_tab", self.home_tab),
            # ("equities", self.equities),
            ("it_sector", self.it_sector),
            ("auto_sector", self.auto_sector),
            ("telecom_sector", self.telecom_sector),
            ("pharma_sector", self.pharma_sector),
            ("healthcare_sector", self.healthcare_sector),
            ("banking_sector", self.banking_sector),
            ("energy_sector", self.energy_sector),
            ("fmcg_sector", self.fmcg_sector),
            ("finance_sector", self.finance_sector),

        ]
        for name, locator in elements:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(locator)
                ).click()

                status = "pass"
                actual_error = ""

            except Exception as e:
                status = "fail"
                actual_error = "XPath not found or invalid xpath"

            test_results.append({
                "Page": "Dashboard",
                "Testing_Area": name,
                "expected": expected,
                "actual": f"{name} are clicked successfully" if status == "pass" else actual_error,
                "status": status
            })

        back_menu = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='cursor-pointer flex items-center']//*[name()='svg']"))
        )
        back_menu.click()
        time.sleep(7)

    def etf_button(self, test_results, expected="pass"):
        elements = [
            ("etf", self.etf),
            ("index", self.index),
            ("equity", self.equity),
            ("sector", self.sector),
            ("gold", self.sector),
            ("debt", self.debt),
            ("global", self.global_),

        ]
        for name, locator in elements:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(locator)
                ).click()

                status = "pass"
                actual_error = ""

            except Exception as e:
                status = "fail"
                actual_error = "XPath not found or invalid xpath"

            test_results.append({
                "Page": "Dashboard",
                "Testing_Area": name,
                "expected": expected,
                "actual": f"{name} tab clicked successfully" if status == "pass" else actual_error,
                "status": status
            })

        back_menu = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//p[contains(normalize-space(),'Home')]"))
        )
        back_menu.click()
        time.sleep(7)

    def ipo_button(self, test_results, expected="pass"):
        elements = [
            ("etf", self.ipo),
            ("ongoing", self.ongoing),
            ("ipo_applied", self.ipo_applied),
            ("recently_listed", self.recently_listed),
            ("announced", self.announced),

        ]
        for name, locator in elements:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(locator)
                ).click()

                status = "pass"
                actual_error = ""

            except Exception as e:
                status = "fail"
                actual_error = "XPath not found or invalid xpath"

            test_results.append({
                "Page": "Dashboard",
                "Testing_Area": name,
                "expected": expected,
                "actual": f"{name} tab clicked successfully" if status == "pass" else actual_error,
                "status": status
            })

        back_menu = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//p[contains(normalize-space(),'Home')]"))
        )
        back_menu.click()
        time.sleep(7)

    def screeners_button(self, test_results, expected="pass"):
        elements = [
            ("screeners", self.screeners),
            ("top_gainers", self.top_gainer),
            ("top_looser", self.top_looser),
            ("week_high", self.week_high),
            ("week_low", self.week_low),
            ("rider", self.rider),
            ("dragger", self.dragger),
            ("top_volume", self.top_volume),

        ]
        for name, locator in elements:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(locator)
                ).click()

                status = "pass"
                actual_error = ""

            except Exception as e:
                status = "fail"
                actual_error = "XPath not found or invalid xpath"

            test_results.append({
                "Page": "Dashboard",
                "Testing_Area": name,
                "expected": expected,
                "actual": f"{name} tab clicked successfully" if status == "pass" else actual_error,
                "status": status
            })

        back_menu = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//p[contains(normalize-space(),'Home')]"))
        )
        back_menu.click()
        time.sleep(7)

    def funds_dashboard(self, test_results, expected="pass"):
        elements = [
            ("payin_button", self.payin_button),
            ("home_path", self.home_path)
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
                "Page": "Dashboard",
                "Testing_Area": name,
                "expected": expected,
                "actual": f"{name} tab clicked successfully" if status == "pass" else actual_error,
                "status": status
            })

        time.sleep(7)

    def holdings_dashboard(self, test_results, expected="pass"):
        elements = [
            ("holdings_path", self.holdings_path),
            ("home_path", self.home_path)
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
                "Page": "Dashboard",
                "Testing_Area": name,
                "expected": expected,
                "actual": f"{name} tab clicked successfully" if status == "pass" else actual_error,
                "status": status
            })

        time.sleep(7)

    def chart_indication(self, test_results, expected="pass"):
        elements = [
            ("individual_value", self.individual_value),
            ("investment_value", self.investment_value),
            ("pnl_value", self.pnl_value)
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
                "Page": "Dashboard",
                "Testing_Area": name,
                "expected": expected,
                "actual": f"{name} tab clicked successfully" if status == "pass" else actual_error,
                "status": status
            })

        time.sleep(7)

    def snapAlpha_(self, test_results, expected="pass"):
        elements = [
            ("option_chain", self.option_chain_snapAlpha),
            ("scalper", self.scalper_snapAlpha),
        ]
        for name, locator in elements:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(locator)
                ).click()

                status = "pass"
                actual_error = ""

            except Exception as e:
                status = "fail"
                actual_error = "XPath not found or invalid xpath"

            test_results.append({
                "Page": "Dashboard",
                "Testing_Area": name,
                "expected": expected,
                "actual": f"{name} tab clicked successfully" if status == "pass" else actual_error,
                "status": status
            })

        # back_menu = WebDriverWait(self.driver, 5).until(
        #     EC.element_to_be_clickable((By.XPATH, "//p[contains(normalize-space(),'Home')]"))
        # )
        # back_menu.click()
        time.sleep(7)
        ''

    def research_Ideas(self, test_results, expected="pass"):
        elements = [
            ("research_ideas_viewAll", self.research_ideas_viewAll),
        ]
        for name, locator in elements:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(locator)
                ).click()

                status = "pass"
                actual_error = ""

            except Exception as e:
                status = "fail"
                actual_error = "XPath not found or invalid xpath"

            test_results.append({
                "Page": "Dashboard",
                "Testing_Area": name,
                "expected": expected,
                "actual": f"{name} tab clicked successfully" if status == "pass" else actual_error,
                "status": status
            })

        # back_menu = WebDriverWait(self.driver, 5).until(
        #     EC.element_to_be_clickable((By.XPATH, "//p[contains(normalize-space(),'Home')]"))
        # )
        # back_menu.click()
        time.sleep(7)

    def sub_button(self, test_results, expected="pass"):
        elements = [
            ("intraday_subtab", self.intraday_sub_tab),
            ("delivery_sub_tab", self.delivery_sub_tab),

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
                "Page": "Dashboard",
                "Testing_Area": name,
                "expected": expected,
                "actual": "clicked successfully" if status == "pass" else actual_error,
                "status": status
            })

    def commodity_button(self, test_results, expected="pass"):
        elements = [
            ("commodity_tab", self.commodity_tab),
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
                "Page": "Dashboard",
                "Testing_Area": name,
                "expected": expected,
                "actual": "clicked successfully" if status == "pass" else actual_error,
                "status": status
            })

    def basket_button_(self, test_results, expected="pass"):
        elements = [

            ("basket_button", self.basket_button),
            ("invest_button", self.invest_button),
            ("back_button", self.back_button)
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
                "Page": "Dashboard",
                "Testing_Area": name,
                "expected": expected,
                "actual": "clicked successfully" if status == "pass" else actual_error,
                "status": status
            })

    def basket_fno_button_(self, test_results, expected="pass"):
        elements = [
            ("basket_FNO_button", self.basket_FNO_button)
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
                "Page": "Dashboard",
                "Testing_Area": name,
                "expected": expected,
                "actual": "clicked successfully" if status == "pass" else actual_error,
                "status": status
            })

    def back_button_research(self, test_results, expected="pass"):
        elements = [
            ("back_button_", self.back_button_)
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
                "Page": "Dashboard",
                "Testing_Area": name,
                "expected": expected,
                "actual": "clicked successfully" if status == "pass" else actual_error,
                "status": status
            })
