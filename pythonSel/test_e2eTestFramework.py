import csv
# pytest -m smoke   // Tagging
# pytest -n 10 //pytest-xdist plugin you need to run in parallel

# pytest -n 2 -m smoke --browser_name firefox --html=reports/report.html

import os
import sys
import time
import pytest
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException, InvalidSelectorException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains, Keys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pageObjects.login import LoginData
from pageObjects.otp import otpPage
from pageObjects.mutual_fund import MutualFundPage
from pageObjects.funds import FundsPage
from pageObjects.explore import ExplorePage
from pageObjects.watchlist import WatchList
from pageObjects.orders import OrderBook
from pageObjects.holdings import HoldingsPage
from pageObjects.positions import PositionPage
from pageObjects.order_window_buy import orderWindowPage
from pageObjects.dashboard import DashboardPage
from pageObjects.predefined_watchlist import predefinedWatchList
from pageObjects.profile import ProfilePage

test_results = []


@pytest.mark.parametrize("username,password,expected", [
    # ("TEST109", "Admin@123", "pass"),
    # ("L2020", "Asd@123", "fail")
    ("DVJ7126", "Akash@#3", "pass"),
    # ("DVJ7126", "Akash@#3", "pass"),
    # ("MUL708", "Abc@1234", "pass"),
])
def test_login_scenarios(browserInstance, username, password, expected):
    driver = browserInstance
    loginPage = LoginData(driver)

    try:
        loginPage.login(username, password)
    except Exception as e:
        print(f"❌ Login function failed: {e}")
        driver.save_screenshot(f"reports/login_error_{username}.png")
        raise

    actual_error = loginPage.get_login_error()
    print(f"Actual error message: {actual_error}")

    status = "fail" if actual_error else "pass"

    test_results.append({
        "username": username,
        "password": password,
        "expected": expected,
        "actual": "login success" if not actual_error else f"error: {actual_error}",
        "status": status
    })

    driver.save_screenshot(f"reports/login_{username}_{status}.png")
    assert status == expected, f"❌ Test Failed: expected {expected}, got {status}"


@pytest.mark.parametrize("otpvalue,expected", [
    ("123456", "pass"),
])
def test_login_otp(browserInstance, otpvalue, expected):
    driver = browserInstance

    # reset_application(driver)

    otppage = otpPage(driver)
    try:
        otppage.get_otp(str(otpvalue))
    except RuntimeError as e:
        if "delegate" in str(e) or "dynamic-sized tensors" in str(e):
            raise AssertionError(f"TFLite crash for {otpvalue} - Tensor size mismatch") from e
        else:
            raise

    actual_error = otppage.get_login_error()

    if actual_error:
        actual_result = "fail"
        actual_message = "error shown"
    else:
        actual_result = "pass"
        actual_message = "OTP validated successfully"

    test_results.append({
        "otp": otpvalue,
        "expected": expected,
        "actual": actual_message,
        "status": "pass" if actual_result == expected else "fail"
    })

    print(test_results)
    assert actual_result == expected


def click_close_icon(driver, timeout=5):
    """Safely click the close (X) icon if visible."""
    wait = WebDriverWait(driver, timeout)
    close_icon_xpath = "//div[@class='cursor-pointer' and descendant::svg[@stroke-width='1.5']]"
    try:
        close_icon = wait.until(EC.element_to_be_clickable((By.XPATH, close_icon_xpath)))
        driver.execute_script("arguments[0].click();", close_icon)
        print("✅ Clicked on close (X) icon successfully.")
        time.sleep(1)
    except Exception:
        print("ℹ️ No close icon visible or already closed.")


def append_result(area, expected, actual, status):
    test_results.append({
        "Page": "Watchlist",
        "Testing_Area": area,
        "expected": expected,
        "actual": actual,
        "status": status
    })


# @pytest.mark.parametrize("search_scrip,expected", [
#     ("ACCELYA", "pass"),
#     ("FEB 25000 CE", "pass"),
#     ("FEB 25000 PE", "pass"),
#     ("CRUDEOIL", "pass"),
#     ("JEERAMINI", "pass"),
# ])
# def test_watchlist_scenarios(browserInstance, search_scrip, expected):
#     driver = browserInstance
#     wait = WebDriverWait(driver, 10)
#     actions = ActionChains(driver)
#     WatchListData = LoginData(driver)
#     try:
#         search_input = wait.until(EC.visibility_of_element_located((By.ID, "default-search")))
#         search_input.clear()
#         search_input.send_keys(search_scrip)
#
#         time.sleep(1.5)  # Let suggestions load
#
#         test_results.append({
#             "Page": "Watchlist",
#             "Testing_Area": f"Scrip Search - {search_scrip}",
#             "expected": "Scrip should be searchable",
#             "actual": "Scrip searched successfully",
#             "status": "pass"
#         })
#     except Exception as e:
#         test_results.append({
#             "Page": "Watchlist",
#             "Testing_Area": f"Scrip Search - {search_scrip}",
#             "expected": "Scrip should be searchable",
#             "actual": str(e),
#             "status": "fail"
#         })
#         assert False
#     time.sleep(1.5)
#     try:
#
#         scrip_xpath = f"//div[contains(@id,'_search_scrip')]//div[@class='text-[14px]' and contains(normalize-space(),'{search_scrip}')]"
#         scrip_element = wait.until(EC.element_to_be_clickable((By.XPATH, scrip_xpath)))
#         driver.execute_script("arguments[0].scrollIntoView(true);", scrip_element)
#         scrip_element.click()
#         print(f"✅ Clicked on scrip: {search_scrip}")
#
#         test_results.append({
#             "Page": "Watchlist",
#             "Testing_Area": f"Scrip Selection - {search_scrip}",
#             "expected": "Scrip should be selectable",
#             "actual": "Scrip clicked successfully",
#             "status": "pass"
#         })
#     except Exception as e:
#         test_results.append({
#             "Page": "Watchlist",
#             "Testing_Area": f"Scrip Selection - {search_scrip}",
#             "expected": "Scrip should be selectable",
#             "actual": str(e),
#             "status": "fail"
#         })
#         assert False
#     time.sleep(1.5)
#     try:
#
#         # --- Step 3: Click the '+' (Add to watchlist) button ---
#         add_button_xpath = f"{scrip_xpath}/ancestor::div[contains(@id,'_search_scrip')]//button[contains(@class,'bg-purple-600')]"
#         add_button = wait.until(EC.element_to_be_clickable((By.XPATH, add_button_xpath)))
#         driver.execute_script("arguments[0].click();", add_button)
#         print(f"✅ Added scrip '{search_scrip}' to Watchlist")
#
#         test_results.append({
#             "Page": "Watchlist",
#             "Testing_Area": f"Add Scrip - {search_scrip}",
#             "expected": "Scrip should be added to watchlist",
#             "actual": "Scrip added successfully",
#             "status": "pass"
#         })
#     except Exception as e:
#         test_results.append({
#             "Page": "Watchlist",
#             "Testing_Area": f"Add Scrip - {search_scrip}",
#             "expected": "Scrip should be added to watchlist",
#             "actual": str(e),
#             "status": "fail"
#         })
#         assert False
#     click_close_icon(driver)  # close any confirmation popup
#
#     try:
#         success_toast_xpath = "//div[contains(@class,'toast') or contains(@class,'notification')]"
#         success_message = wait.until(EC.presence_of_element_located((By.XPATH, success_toast_xpath)))
#         print("✅ Detected success message after adding scrip:", success_message.text)
#         actual_result = "pass"
#         # confirmation_xpath = f"//div[contains(@class,'watchlist')]//*[contains(text(),'{search_scrip}')]"
#         # wait.until(EC.presence_of_element_located((By.XPATH, confirmation_xpath)))
#         # actual_result = "pass"
#         # print(f"✅ Verified '{search_scrip}' added successfully.")
#     except Exception:
#         # Fallback: Look for the scrip in the watchlist section (in case no toast)
#         try:
#             watchlist_xpath = f"//*[contains(text(),'{search_scrip}') and not(contains(@id,'_search_scrip'))]"
#             wait.until(EC.presence_of_element_located((By.XPATH, watchlist_xpath)))
#             print(f"✅ Verified '{search_scrip}' added to watchlist.")
#             actual_result = "pass"
#         except Exception:
#             print(f"❌ '{search_scrip}' not found in watchlist or confirmation toast.")
#             actual_result = "fail"
#
#     # --- Step 5: Assert expected vs actual ---
#     assert actual_result == expected, f"Expected '{expected}', but got '{actual_result}' for {search_scrip}"


#
#
# def test_watchlist_predefined(browserInstance):
#     driver = browserInstance
#     wait = WebDriverWait(driver, 20)
#     predefined_watchlist = predefinedWatchList(driver)
#     expected = "pass"
#
#     try:
#         time.sleep(2)
#         predefined_watchlist.predefined_watchlist_tab(test_results, expected)
#         time.sleep(2)
#     except Exception as e:
#         print(e)


# def test_watchlist_settings(browserInstance):
#     driver = browserInstance
#     wait = WebDriverWait(driver, 20)
#     watchlist_Settings = WatchList(driver)
#     expected = "pass"
#
#     try:
#         time.sleep(2)
#         watchlist_Settings.watchlist_setting(test_results, expected)
#         time.sleep(2)
#     except Exception as e:
#         print(e)
#
#
# def test_mutual_fund(browserInstance):
#     driver = browserInstance
#     wait = WebDriverWait(driver, 20)
#     mutual_fund = MutualFundPage(driver)
#     expected = "pass"
#
#     try:
#         time.sleep(2)
#         mutual_fund.mutual_fund_page(test_results, expected)
#         time.sleep(2)
#         # mutual_fund.mutual_fund_orders(test_results, expected)
#         # mutual_fund.mutual_fund_watchlist(test_results, expected)
#     except Exception as e:
#         print(e)


# @pytest.mark.parametrize("search_scrip,expected", [
#     ("Nippon India Multi Asset", "pass"),
# ])
# def test_watchlist_scenarios_mf(browserInstance, search_scrip, expected):
#     driver = browserInstance
#     wait = WebDriverWait(driver, 10)
#     actions = ActionChains(driver)
#     WatchListData = LoginData(driver)
#     try:
#         search_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='default-search']")))
#         search_input.clear()
#         search_input.send_keys(search_scrip)
#
#         time.sleep(1.5)  # Let suggestions load
#
#         test_results.append({
#             "Page": "Mutual Fund",
#             "Testing_Area": f"Scrip Search - {search_scrip}",
#             "expected": "Scrip should be searchable",
#             "actual": "Scrip searched successfully",
#             "status": "pass"
#         })
#     except Exception as e:
#         test_results.append({
#             "Page": "Mutual Fund",
#             "Testing_Area": f"Scrip Search - {search_scrip}",
#             "expected": "Scrip should be searchable",
#             "actual": str(e),
#             "status": "fail"
#         })
#         assert False
#     time.sleep(1.5)
#     try:
#
#         scrip_xpath = f"//div[contains(@id,'_search_scrip')]//div[@class='text-[14px]' and contains(normalize-space(),'{search_scrip}')]"
#         scrip_element = wait.until(EC.element_to_be_clickable((By.XPATH, scrip_xpath)))
#         driver.execute_script("arguments[0].scrollIntoView(true);", scrip_element)
#         scrip_element.click()
#         print(f"✅ Clicked on scrip: {search_scrip}")
#
#         test_results.append({
#             "Page": "Mutual Fund",
#             "Testing_Area": f"Scrip Selection - {search_scrip}",
#             "expected": "Scrip should be selectable",
#             "actual": "Scrip clicked successfully",
#             "status": "pass"
#         })
#     except Exception as e:
#         test_results.append({
#             "Page": "Mutual Fund",
#             "Testing_Area": f"Scrip Selection - {search_scrip}",
#             "expected": "Scrip should be selectable",
#             "actual": str(e),
#             "status": "fail"
#         })
#         assert False
#     time.sleep(1.5)
#     try:
#
#         # --- Step 3: Click the '+' (Add to watchlist) button ---
#         add_button_xpath = f"{scrip_xpath}/ancestor::div[contains(@id,'_search_scrip')]//button[contains(@class,'bg-purple-600')]"
#         add_button = wait.until(EC.element_to_be_clickable((By.XPATH, add_button_xpath)))
#         driver.execute_script("arguments[0].click();", add_button)
#         print(f"✅ Added scrip '{search_scrip}' to Watchlist")
#         close_icon = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'cursor-pointer')][.//svg]")))
#         close_icon.click()
#
#         test_results.append({
#             "Page": "Mutual Fund",
#             "Testing_Area": f"Add Scrip - {search_scrip}",
#             "expected": "Scrip should be added to watchlist",
#             "actual": "Scrip added successfully",
#             "status": "pass"
#         })
#     except Exception as e:
#         test_results.append({
#             "Page": "Mutual Fund",
#             "Testing_Area": f"Add Scrip - {search_scrip}",
#             "expected": "Scrip should be added to watchlist",
#             "actual": str(e),
#             "status": "fail"
#         })
#         assert False
#     click_close_icon(driver)  # close any confirmation popup
#
#     try:
#         success_toast_xpath = "//div[contains(@class,'toast') or contains(@class,'notification')]"
#         success_message = wait.until(EC.presence_of_element_located((By.XPATH, success_toast_xpath)))
#         print("✅ Detected success message after adding scrip:", success_message.text)
#         actual_result = "pass"
#         # confirmation_xpath = f"//div[contains(@class,'watchlist')]//*[contains(text(),'{search_scrip}')]"
#         # wait.until(EC.presence_of_element_located((By.XPATH, confirmation_xpath)))
#         # actual_result = "pass"
#         # print(f"✅ Verified '{search_scrip}' added successfully.")
#     except Exception:
#         # Fallback: Look for the scrip in the watchlist section (in case no toast)
#         try:
#             watchlist_xpath = f"//*[contains(text(),'{search_scrip}') and not(contains(@id,'_search_scrip'))]"
#             wait.until(EC.presence_of_element_located((By.XPATH, watchlist_xpath)))
#             print(f"✅ Verified '{search_scrip}' added to watchlist.")
#             actual_result = "pass"
#         except Exception:
#             print(f"❌ '{search_scrip}' not found in watchlist or confirmation toast.")
#             actual_result = "fail"
#
#     # --- Step 5: Assert expected vs actual ---
#     assert actual_result == expected, f"Expected '{expected}', but got '{actual_result}' for {search_scrip}"


@pytest.mark.usefixtures("browserInstance")
def test_order_window(browserInstance):
    driver = browserInstance
    expected = "pass"
    wait = WebDriverWait(driver, 20)
    order_window = orderWindowPage(driver)
    order_window.orderWindow(test_results, expected)
    order_window.orderWindow_Sell(test_results, expected)
    time.sleep(3)


#
# @pytest.mark.usefixtures("browserInstance")
# def test_order_list(browserInstance):
#     driver = browserInstance
#     expected = "pass"
#     wait = WebDriverWait(driver, 20)
#     order_list_ = OrderBook(driver)
#     order_list_.order_button(test_results, expected)
#     time.sleep(12)


# order_list_.order_list(test_results, expected)


#
# # @pytest.mark.usefixtures("browserInstance")
# # def test_pending_order_list(browserInstance):
# #     driver = browserInstance
# #     expected = "pass"
# #     wait = WebDriverWait(driver, 20)
# #     order_list_ = OrderBook(driver)
# #     order_list_.order_button_pending(test_results, expected)
# #     time.sleep(12)
# #     order_list_.pending_order_list()
# #     time.sleep(2)
# #     order_window = orderWindowPage(driver)
# #     order_window.pending_order_fun()
#
#
# #
#
#
# #
#
# #
#
#

# @pytest.mark.usefixtures("browserInstance")
# def test_dashboard(browserInstance):
#     driver = browserInstance
#     expected = "pass"
#     wait = WebDriverWait(driver, 20)
#     dashboard_list = DashboardPage(driver)
#     # dashboard_list.equity_button(test_results, expected)
#     dashboard_list.etf_button(test_results, expected)
#     dashboard_list.ipo_button(test_results, expected)
#     dashboard_list.screeners_button(test_results, expected)
#     dashboard_list.funds_dashboard(test_results, expected)
#     dashboard_list.holdings_dashboard(test_results, expected)
#     dashboard_list.chart_indication(test_results, expected)
#     dashboard_list.snapAlpha_(test_results, expected)
#     dashboard_list.research_Ideas(test_results, expected)
#     dashboard_list.sub_button(test_results, expected)
#     dashboard_list.commodity_button(test_results, expected)
#     dashboard_list.basket_button_(test_results, expected)
#     dashboard_list.basket_fno_button_(test_results, expected)
#     dashboard_list.back_button_research(test_results, expected)


#
# #
# #
# @pytest.mark.usefixtures("browserInstance")
# def test_gtt_order_list(browserInstance):
#     driver = browserInstance
#     expected = "pass"
#     wait = WebDriverWait(driver, 20)
#     order_list_ = OrderBook(driver)
#     # order_list_.gtt_order_button(test_results, expected)
#     order_list_.basket_order_button(test_results, expected)
# order_list_.sip_button(test_results, expected)
# order_window = orderWindowPage(driver)
# order_window.pending_order_fun()

#
# @pytest.mark.usefixtures("browserInstance")
# def test_position(browserInstance):
#     driver = browserInstance
#     expected = "pass"
#     wait = WebDriverWait(driver, 20)
#     position_list_ = PositionPage(driver)
#     position_list_.position_button(test_results, expected)


# # position_list_.position_list(test_results, expected)
#

# @pytest.mark.usefixtures("browserInstance")
# def test_holding(browserInstance):
#     driver = browserInstance
#     expected = "pass"
#     wait = WebDriverWait(driver, 20)
#     holding_list_ = HoldingsPage(driver)
#     holding_list_.stocks_button(test_results, expected)


# # holding_list_.holdings_list()
#
#
# #
# @pytest.mark.usefixtures("browserInstance")
# def test_funds(browserInstance):
#     driver = browserInstance
#     expected = "pass"
#     wait = WebDriverWait(driver, 20)
#     funds_page = FundsPage(driver)
#     funds_page.funds_button(test_results, expected)


# @pytest.mark.usefixtures("browserInstance")
# def test_profile(browserInstance):
#     driver = browserInstance
#     expected = "pass"
#     wait = WebDriverWait(driver, 20)
#     profile_list = ProfilePage(driver)
#     profile_list.profile_button(test_results, expected)
#     profile_list.profile_toggle(test_results, expected)
#     profile_list.bo_reports(test_results, expected)
#     profile_list.reports_(test_results, expected)


@pytest.mark.usefixtures("browserInstance")
def test_click_first_watchlist_scrip(browserInstance):
    driver = browserInstance
    wait = WebDriverWait(driver, 15)

    # --- Step 1: Wait until the first scrip appears ---
    # first_scrip_xpath = "//div[contains(@id,'|NFO') or contains(@id,'|EQ')][1]"
    # first_scrip = wait.until(EC.visibility_of_element_located((By.XPATH, first_scrip_xpath)))
    # driver.execute_script("arguments[0].scrollIntoView({block:'center'});", first_scrip)
    # print("✅ First scrip located")

    scrip_items = driver.find_elements(By.XPATH,
                                       "//div[contains(@class, 'border-b') and contains(@class, 'bgCardColor') and contains(@id, '|NSE')]")

    if not scrip_items:
        append_result(
            "Watchlist Scrip Presence",
            "At least one scrip should be present in watchlist",
            "No scrip found in watchlist",
            "fail"
        )
        return
    else:
        append_result(
            "Watchlist Scrip Presence",
            "At least one scrip should be present in watchlist",
            "Scrip found in watchlist",
            "pass"
        )

    scrip = scrip_items[0]  # Only first scrip

    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", scrip)
        ActionChains(driver).move_to_element(scrip).perform()
        time.sleep(1)

        buy_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='B']")
        buy_button.click()
        append_result("Buy Button", "Buy window should open", "Buy clicked successfully", "pass")

        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='ml-2 cursor-pointer']//*[name()='svg']"))).click()
        append_result("Buy Cancel", "Buy window should close", "Buy cancelled successfully", "pass")

    except Exception as e:
        append_result("Buy Flow", "Buy flow should work", str(e), "fail")

    try:
        ActionChains(driver).move_to_element(scrip).perform()
        sell_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='S']")
        sell_button.click()
        append_result("Sell Button", "Sell window should open", "Sell clicked successfully", "pass")

        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='ml-2 cursor-pointer']//*[name()='svg']"))).click()
        append_result("Sell Cancel", "Sell window should close", "Sell cancelled successfully", "pass")

    except Exception as e:
        append_result("Sell Flow", "Sell flow should work", str(e), "fail")

    try:
        ActionChains(driver).move_to_element(scrip).perform()
        chart_buttons = scrip.find_elements(By.XPATH, ".//button")

        if len(chart_buttons) >= 3:
            chart_buttons[2].click()
            append_result("Chart", "Chart should open", "Chart opened successfully", "pass")
        else:
            append_result("Chart", "Chart button should be present", "Chart button not found", "fail")

    except Exception as e:
        append_result("Chart", "Chart should open", str(e), "fail")

    try:
        ActionChains(driver).move_to_element(scrip).perform()
        depth_button = scrip.find_element(By.XPATH, ".//button[contains(@class,'outlined_btn')][2]")
        depth_button.click()
        append_result("Depth", "Depth should open", "Depth opened successfully", "pass")

        depth_button.click()
        append_result("Depth Close", "Depth should close", "Depth closed successfully", "pass")
        time.sleep(9)
    except Exception as e:
        append_result("Depth Flow", "Depth toggle should work", str(e), "fail")

    try:
        ActionChains(driver).move_to_element(scrip).perform()
        menu_button = scrip.find_element(By.XPATH, ".//button[contains(@id, '_opt_btn')]")
        menu_button.click()

        info_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[normalize-space()='Info']/ancestor::button")))
        info_button.click()
        append_result("Info", "Info popup should open", "Info opened successfully", "pass")

        close_info = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Close']")))
        close_info.click()
        append_result("Info Close", "Info popup should close", "Info closed successfully", "pass")

    except Exception as e:
        append_result("Info Flow", "Info flow should work", str(e), "fail")

    try:
        ActionChains(driver).move_to_element(scrip).perform()
        menu_button = scrip.find_element(By.XPATH, ".//button[contains(@id, '_opt_btn')]")
        menu_button.click()

        info_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[normalize-space()='Info']/ancestor::button")))
        info_button.click()
        append_result("Info", "Info popup should open", "Info opened successfully", "pass")

        close_info = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Close']")))
        close_info.click()
        append_result("Info Close", "Info popup should close", "Info closed successfully", "pass")

    except Exception as e:
        append_result("Info Flow", "Info flow should work", str(e), "fail")

    try:
        ActionChains(driver).move_to_element(scrip).perform()
        menu_button = scrip.find_element(By.XPATH, ".//button[contains(@id, '_opt_btn')]")
        menu_button.click()

        create_alert_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[normalize-space()='Create Alerts']/ancestor::button")))
        create_alert_button.click()
        append_result("Create Alert", "Alert popup should open", "Alert opened successfully", "pass")

        alert_close_button = wait.until(EC.element_to_be_clickable((By.ID, "close_alert_btn")))
        alert_close_button.click()
        append_result("Create Alert Close", "Alert popup should close", "Alert closed successfully", "pass")

    except Exception as e:
        append_result("Create Alert Flow", "Alert flow should work", str(e), "fail")

    try:
        ActionChains(driver).move_to_element(scrip).perform()
        menu_button = scrip.find_element(By.XPATH, ".//button[contains(@id, '_opt_btn')]")
        menu_button.click()

        create_gtt_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[normalize-space()='Create GTT']/ancestor::button")))
        create_gtt_button.click()
        append_result("Create GTT", "GTT popup should open", "GTT opened successfully", "pass")

        gtt_close_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Cancel']")))
        gtt_close_button.click()
        append_result("Create GTT Close", "GTT popup should close", "GTT closed successfully", "pass")

    except Exception as e:
        append_result("Create GTT Flow", "GTT flow should work", str(e), "fail")
    # try:
    #     ActionChains(driver).move_to_element(scrip).perform()
    #     menu_button = scrip.find_element(By.XPATH, ".//button[contains(@id, '_opt_btn')]")
    #     menu_button.click()
    #
    #     option_chain_button = wait.until(EC.element_to_be_clickable(
    #         (By.XPATH, "//span[normalize-space()='Option Chain']/ancestor::button")))
    #     option_chain_button.click()
    #     append_result("Option Chain", "Option Chain should open", "Option Chain opened successfully", "pass")
    #
    # except Exception as e:
    #     append_result("Option Chain", "Option Chain should open", str(e), "fail")

    # try:
    #     print("=== Working on First Scrip ===")
    #     driver.execute_script("arguments[0].scrollIntoView(true);", scrip)
    #     ActionChains(driver).move_to_element(scrip).perform()
    #     time.sleep(1)
    #
    #     # === Click Buy ===
    #     buy_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='B']")
    #     buy_button.click()
    #     print("🟢 Clicked Buy")
    #     wait.until(
    #         EC.element_to_be_clickable((By.XPATH, "//div[@class='ml-2 cursor-pointer']//*[name()='svg']"))).click()
    #     print("❎ Cancelled Buy")
    #     time.sleep(1)
    #
    #     # === Click Sell ===
    #     ActionChains(driver).move_to_element(scrip).perform()
    #     sell_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='S']")
    #     sell_button.click()
    #     print("🔴 Clicked Sell")
    #     wait.until(
    #         EC.element_to_be_clickable((By.XPATH, "//div[@class='ml-2 cursor-pointer']//*[name()='svg']"))).click()
    #     print("❎ Cancelled Sell")
    #     time.sleep(1)
    #
    #     # === Click Chart ===
    #     ActionChains(driver).move_to_element(scrip).perform()
    #     chart_buttons = scrip.find_elements(By.XPATH, ".//button")
    #     if len(chart_buttons) >= 3:
    #         chart_buttons[2].click()
    #         print("📊 Clicked Chart")
    #         time.sleep(2)
    #
    #     ActionChains(driver).move_to_element(scrip).perform()
    #     depth_button = scrip.find_element(By.XPATH, ".//button[contains(@class,'outlined_btn')][2]")
    #     depth_button.click()
    #     print("☰ Opened More Options")
    #     time.sleep(1)
    #
    #     ActionChains(driver).move_to_element(scrip).perform()
    #     depth_button_close = scrip.find_element(By.XPATH, ".//button[contains(@class,'outlined_btn')][2]")
    #     depth_button_close.click()
    #     print("☰ Opened More Options")
    #     time.sleep(1)
    #
    #     # === Click 3-dot menu (More Options) ===
    #     ActionChains(driver).move_to_element(scrip).perform()
    #     menu_button = scrip.find_element(By.XPATH, ".//button[contains(@id, '_opt_btn')]")
    #     menu_button.click()
    #     print("☰ Opened More Options")
    #     time.sleep(1)
    #
    #     # === Click Info and close popup ===
    #     info_button = wait.until(EC.element_to_be_clickable(
    #         (By.XPATH, "//span[normalize-space()='Info']/ancestor::button")))
    #     info_button.click()
    #     print("ℹ️ Clicked Info")
    #     time.sleep(2)
    #
    #     close_info = wait.until(EC.element_to_be_clickable((
    #         By.XPATH, "//button[normalize-space(text())='Close']")))
    #     close_info.click()
    #     print("❎ Closed Info")
    #
    #     time.sleep(5)
    #     ActionChains(driver).move_to_element(scrip).perform()
    #     menu_button = scrip.find_element(By.XPATH, ".//button[contains(@id, '_opt_btn')]")
    #     menu_button.click()
    #     print("☰ Opened More Options")
    #     time.sleep(1)
    #
    #     create_alert_button = wait.until(EC.element_to_be_clickable(
    #         (By.XPATH, "//span[normalize-space()='Create Alerts']/ancestor::button")))
    #     create_alert_button.click()
    #     print("ℹ️ Clicked Info")
    #     time.sleep(2)
    #
    #     alert_close_button = wait.until(EC.element_to_be_clickable(
    #         (By.ID, "close_alert_btn")))
    #     alert_close_button.click()
    #     print("ℹ️ Clicked Info")
    #     time.sleep(2)
    #
    #     ActionChains(driver).move_to_element(scrip).perform()
    #     menu_button = scrip.find_element(By.XPATH, ".//button[contains(@id, '_opt_btn')]")
    #     menu_button.click()
    #     print("☰ Opened More Options")
    #     time.sleep(1)
    #
    #     create_gtt_button = wait.until(EC.element_to_be_clickable(
    #         (By.XPATH, "//span[normalize-space()='Create GTT']/ancestor::button")))
    #     create_gtt_button.click()
    #     print("ℹ️ Clicked Info")
    #     time.sleep(2)
    #
    #     gtt_close_button = wait.until(EC.element_to_be_clickable(
    #         (By.XPATH, "//button[normalize-space()='Cancel']")))
    #     gtt_close_button.click()
    #     print("ℹ️ Clicked Info")
    #     time.sleep(2)
    #
    #     ActionChains(driver).move_to_element(scrip).perform()
    #     menu_button = scrip.find_element(By.XPATH, ".//button[contains(@id, '_opt_btn')]")
    #     menu_button.click()
    #     print("☰ Opened More Options")
    #     time.sleep(1)
    #
    #     option_chain_button = wait.until(EC.element_to_be_clickable(
    #         (By.XPATH, "//span[normalize-space()='Option Chain']/ancestor::button")))
    #     option_chain_button.click()
    #     print("ℹ️ Clicked Info")
    #     time.sleep(2)
    #
    #     ActionChains(driver).move_to_element(scrip).perform()
    #     menu_button = scrip.find_element(By.XPATH, ".//button[contains(@id, '_opt_btn')]")
    #     menu_button.click()
    #     print("☰ Opened More Options")
    #     time.sleep(1)
    #
    #
    #
    # except Exception as e:
    #     print("❌ Error while processing first scrip:", e)


if __name__ == "__main__":
    pytest.main(["-v", "test_e2eTestFramework.py"])
