import time

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from utils.browserutils import BrowserUtils
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pageObjects.dashboard import DashboardPage

from pageObjects.helpers import Helpers


# -*- coding: utf-8 -*-

class orderWindowPage(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.dashboard = DashboardPage(driver)
        self.helpers = Helpers(driver)
        self.ow_regular_tab = (By.XPATH, '//nav[@id="order_tabs"]//button[text()="Regular"]')
        # self.ow_boco_tab = (By.XPATH, '//button[contains(text(), "BO/CO") and contains(@class, "commonInActiveTab")]')
        # self.ow_gtt_tab = (By.XPATH, '//nav[@id="order_tabs"]//button[text()="GTT"]')
        self.ow_normal_tab = (By.XPATH, '//nav[@id="pcode_tabs"]//button[text()="NRML"]')
        self.ow_intraday_tab = (By.XPATH, '//nav[@id="pcode_tabs"]//button[text()="Intraday"]')
        self.ow_limit_tab = (By.XPATH, '//nav[@id="priceType_tabs"]//button[text()="Limit"]')
        self.ow_market_tab = (By.XPATH, '//nav[@id="priceType_tabs"]//button[text()="Market"]')
        self.ow_stop_loss_tab = (By.XPATH, '//nav[@id="priceType_tabs"]//button[text()="SL"]')
        self.ow_stop_loss_market_tab = (By.XPATH, '//nav[@id="priceType_tabs"]//button[text()="SLM"]')
        self.buy_button = (
            By.XPATH,
            "//button[contains(@class, 'capitalize') and contains(@class, 'green_btn') and span[text()='Buy']]")
        self.confirm_buy = (By.XPATH, "//button[@type='button' and @class='confirm_btn' and text()='Yes']")
        self.confirm_amo = (By.XPATH, "//button[@type='button' and contains(@class, 'confirm_btn') and text()='Yes']")
        self.modify_button = (By.XPATH, "//button[span[text()='Modify']]")
        self.ioc_button = (By.ID, "pcode_1")
        self.qty_input = (By.ID, "qty")
        self.logged_validities = set()

    def orderWindow(self, test_results, expected="pass"):
        driver = self.driver
        wait = WebDriverWait(driver, 12)
        buy_logged = False
        regular_logg = False
        limit_ = False
        advance_options_ = False
        longterm_ = False
        intraday_ = False
        buy_btton_ = False
        stop_loss_ = False
        # cover_ = False
        pending_checkbox_ = False
        target_price_input_ = False
        amo_tab_ = False
        mtf_tab_ = False
        validity_flag = False

        # ===================== SCENARIOS =====================
        scenarios = [
            {
                "tag": "Scenario 1 → Regular + Limit + Intraday + Day",
                "product": "Intraday",
                "validity": "DAY",
                "longterm": False
            },
            {
                "tag": "Scenario 2 → Regular + Limit + Intraday + IOC",
                "product": "Intraday",
                "validity": "IOC",
                "longterm": False
            },
            {
                "tag": "Scenario 3 → Regular + Limit + LongTerm + Day",
                "product": "LongTerm",
                "validity": "DAY",
                "longterm": True
            },
            {
                "tag": "Scenario 4 → Regular + Limit + LongTerm + IOC",
                "product": "LongTerm",
                "validity": "IOC",
                "longterm": True
            }
        ]

        scenarios_sl = [
            {
                "tag": "Scenario 1 → Regular + SL + Intraday + Day",
                "product": "Intraday",
                "validity": "DAY",
                "longterm": False
            },
            {
                "tag": "Scenario 2 → Regular + SL + Intraday + IOC",
                "product": "Intraday",
                "validity": "IOC",
                "longterm": False
            },
            {
                "tag": "Scenario 3 → Regular + SL + LongTerm + Day",
                "product": "LongTerm",
                "validity": "DAY",
                "longterm": True
            },
            {
                "tag": "Scenario 4 → Regular + SL + LongTerm + IOC",
                "product": "LongTerm",
                "validity": "IOC",
                "longterm": True
            }
        ]

        scenarios_cover_order = [
            {
                "tag": "Scenario 1 → Cover + SL + Intraday + Day",
                "product": "Intraday",
                "intraday": True
            },
        ]
        scenarios_cover_order_sl = [
            {
                "tag": "Scenario 1 → Cover + SL + Intraday + Day",
                "product": "Intraday",
                "intraday": True
            },
        ]

        def common_fun():
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='Watchlist3']")))
            element.click()

        def append_result(test_results, page, area, expected, actual, status):
            test_results.append({
                "Page": page,
                "Testing_Area": area,
                "expected": expected,
                "actual": actual,
                "status": status
            })

        # ======================================================
        # FUNCTION → CLICK VALIDITY RADIO BUTTON
        # ======================================================

        def select_validity(validity):
            try:
                print(f"➡ Selecting Validity: {validity}")
                radio_xpath = f"//div[@role='radio' and @aria-label='{validity}']//div[contains(@class,'flex')]"

                option = wait.until(EC.element_to_be_clickable((By.XPATH, radio_xpath)))
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", option)
                driver.execute_script("arguments[0].click();", option)
                if validity not in self.logged_validities:
                    append_result(
                        test_results=test_results,
                        page="Order Window",
                        area=f"{validity} button",
                        expected=f"{validity} button clicked",
                        actual=f"{validity} button clicked successfully",
                        status="pass"
                    )
                    self.logged_validities.add(validity)
            except Exception as e:
                if validity not in self.logged_validities:
                    append_result(
                        test_results=test_results,
                        page="Order Window",
                        area=f"{validity} button",
                        expected=f"{validity} button clicked",
                        actual=str(e),
                        status="fail"
                    )

            print(f"✔ Selected {validity}")
            time.sleep(0.5)

        # ======================================================
        # MAIN LOOP FOR ALL SCENARIOS
        # ======================================================
        for scenario in scenarios:
            print(f"\n===================== {scenario['tag']} =====================")
            try:
                common_fun()
                # Step 1: GET SCRIP AGAIN
                scrip_items = driver.find_elements(
                    By.XPATH,
                    "//div[contains(@class, 'border-b') and contains(@class, 'bgCardColor') and contains(@id, '|NSE')]"
                )

                if not scrip_items:
                    print("❌ No scrip found in watchlist.")
                    return

                scrip = scrip_items[0]
                driver.execute_script("arguments[0].scrollIntoView(true);", scrip)
                ActionChains(driver).move_to_element(scrip).perform()
                time.sleep(1)

                # Click BUY button
                buy_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='B']")
                buy_button.click()
                print("🟢 Order window opened")
                if not buy_logged:
                    test_results.append({
                        "Page": "Order Window",
                        "Testing_Area": "Buy button",
                        "expected": "Buy button clicked",
                        "actual": "Buy button clicked successfully",
                        "order_type": "Buy",
                        "status": "pass"
                    })
                    buy_logged = True

                # Step 2: Click REGULAR
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Regular']"))
                ).click()
                print("✔ Selected Regular")
                if not regular_logg:
                    test_results.append({
                        "Page": "Order Window",
                        "Testing_Area": "Regular tab",
                        "expected": "Regular tab clicked",
                        "actual": "Regular tab clicked successfully",
                        "order_type": "Buy",
                        "status": "pass"
                    })
                    regular_logg = True
                time.sleep(1)

                # Step 3: Click LIMIT
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Limit']"))
                ).click()
                print("✔ Selected Limit")
                if not limit_:
                    test_results.append({
                        "Page": "Order Window",
                        "Testing_Area": "Limit tab",
                        "expected": "Limit tab clicked",
                        "actual": "Limit tab clicked successfully",
                        "order_type": "Buy",
                        "status": "pass"
                    })
                    limit_ = True
                time.sleep(1)

                # Step 4: Click ADVANCED OPTIONS
                wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//div[contains(@class,'cursor-pointer') and contains(text(),'Advanced Options')]")
                    )
                ).click()
                if not advance_options_:
                    test_results.append({
                        "Page": "Order Window",
                        "Testing_Area": "Advance option checkbox",
                        "expected": "Advance option checkbox clicked",
                        "actual": "Advance option checkbox clicked successfully",
                        "order_type": "Buy",
                        "status": "pass"
                    })
                    advance_options_ = True
                print("✔ Advanced Options opened")
                time.sleep(1)

                # ioc = driver.find_element(By.XPATH, "//div[@role='radio' and @aria-label='IOC']")
                # ioc.click()

                # Step 5: Select LONG TERM
                if scenario["longterm"]:
                    wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Long Term']"))
                    ).click()
                    if not longterm_:
                        test_results.append({
                            "Page": "Order Window",
                            "Testing_Area": "Longterm tab",
                            "expected": "Longterm tab clicked",
                            "actual": "Longterm tab clicked successfully",
                            "status": "pass"
                        })
                        longterm_ = True

                    print("✔ Selected Long Term")
                else:
                    wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Intraday']"))
                    ).click()
                    if not intraday_:
                        test_results.append({
                            "Page": "Order Window",
                            "Testing_Area": "Intraday tab",
                            "expected": "Intraday tab clicked",
                            "actual": "Intraday tab clicked successfully",
                            "order_type": "Buy",
                            "status": "pass"
                        })
                        intraday_ = True
                    print("✔ Selected Intraday")
                time.sleep(1)

                # Step 6: Select DAY or IOC using our new function
                select_validity(scenario["validity"])

                try:
                    # Buy button
                    wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Buy']"))
                    ).click()

                    # Yes text (confirmation popup)
                    wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Yes']]"))
                    ).click()

                    # Final Yes / Confirm button (FIXED)
                    # wait.until(
                    #     EC.element_to_be_clickable((
                    #         By.XPATH,
                    #         "//button[contains(@class,'reviewOrderBtn') and .//span[normalize-space()='Yes']]"
                    #     ))
                    # ).click()

                    if not buy_btton_:
                        test_results.append({
                            "Page": "Order Window",
                            "Testing_Area": "Buy button",
                            "expected": "Buy button clicked",
                            "actual": "Buy button clicked and order placed successfully",
                            "order_type": "Buy",
                            "status": "pass"
                        })
                        buy_btton_ = True
                    print("🟢 BUY button clicked")
                    time.sleep(1)
                except Exception as e:
                    if not buy_btton_:
                        test_results.append({
                            "Page": "Order Window",
                            "Testing_Area": "Buy button",
                            "expected": "Xpath not valid",
                            "actual": "Buy button clicked failed",
                            "order_type": "Buy",
                            "status": "fail"
                        })
                        buy_btton_ = True

                time.sleep(1)

                print("\n🎉 All 4 scenarios executed successfully!")

                time.sleep(3)
            except Exception as e:
                print(e)

        for sl_scenario in scenarios_sl:
            print(f"\n===================== {sl_scenario['tag']} =====================")
            common_fun()
            # Step 1: GET SCRIP AGAIN
            scrip_items = driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'border-b') and contains(@class, 'bgCardColor') and contains(@id, '|NSE')]"
            )

            if not scrip_items:
                print("❌ No scrip found in watchlist.")
                return

            scrip = scrip_items[0]
            driver.execute_script("arguments[0].scrollIntoView(true);", scrip)
            ActionChains(driver).move_to_element(scrip).perform()
            time.sleep(1)

            # Click BUY button
            buy_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='B']")
            buy_button.click()
            print("🟢 Order window opened")
            time.sleep(1)

            # Step 2: Click REGULAR
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Regular']"))
            ).click()
            print("✔ Selected Regular")
            time.sleep(1)

            # Step 3: Click LIMIT
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='SL']"))
            ).click()
            if not stop_loss_:
                test_results.append({
                    "Page": "Order Window",
                    "Testing_Area": "Stop loss tab",
                    "expected": "Stop loss tab clicked",
                    "actual": "Stop loss tab clicked successfully",
                    "order_type": "Buy",
                    "status": "pass"
                })
                stop_loss_ = True
            print("✔ Selected Limit")
            time.sleep(1)

            # Step 4: Click ADVANCED OPTIONS
            wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class,'cursor-pointer') and contains(text(),'Advanced Options')]")
                )
            ).click()
            print("✔ Advanced Options opened")
            time.sleep(1)

            # ioc = driver.find_element(By.XPATH, "//div[@role='radio' and @aria-label='IOC']")
            # ioc.click()

            # Step 5: Select LONG TERM
            if sl_scenario["longterm"]:
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Long Term']"))
                ).click()
                print("✔ Selected Long Term")
            else:
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Intraday']"))
                ).click()
                print("✔ Selected Intraday")
            time.sleep(1)

            # Step 6: Select DAY or IOC using our new function
            select_validity(sl_scenario["validity"])

            # Step 7: CLICK BUY
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Buy']"))
            ).click()
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Yes']"))
            ).click()
            print("🟢 BUY button clicked")

            time.sleep(1)

        print("\n🎉 All 4 scenarios executed successfully!")

        for cover_scenario in scenarios_cover_order:
            print(f"\n===================== {cover_scenario['tag']} =====================")
            common_fun()
            # Step 1: GET SCRIP AGAIN
            scrip_items = driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'border-b') and contains(@class, 'bgCardColor') and contains(@id, '|NSE')]"
            )

            if not scrip_items:
                print("❌ No scrip found in watchlist.")
                return

            scrip = scrip_items[0]
            driver.execute_script("arguments[0].scrollIntoView(true);", scrip)
            ActionChains(driver).move_to_element(scrip).perform()

            # Click BUY button
            buy_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='B']")
            buy_button.click()
            print("🟢 Order window opened")

            # Step 2: Click REGULAR
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@id='BO/CO_btn']"))
            ).click()

            print("✔ Selected Cover")
            time.sleep(1)

            # Step 3: Click LIMIT
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Limit']"))
            ).click()
            print("✔ Selected Limit")
            time.sleep(1)

            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='pending_check']"))
            ).click()
            if not pending_checkbox_:
                test_results.append({
                    "Page": "Order Window",
                    "Testing_Area": "Pending checkbox",
                    "expected": "Pending checkbox clicked",
                    "actual": "Pending checkbox clicked successfully",
                    "order_type": "Buy",
                    "status": "pass"
                })
                pending_checkbox_ = True
            print("Target_button")
            time.sleep(1)

            stop_loss_el = wait.until(EC.element_to_be_clickable((By.ID, "firstlegTriggerPrice")))
            stop_loss_el.clear()
            for _ in range(10):
                time.sleep(0.3)
                stop_loss_el.send_keys(Keys.ARROW_UP)

            qty_el = wait.until(EC.element_to_be_clickable((By.ID, "targetPrice")))
            qty_el.clear()
            qty_el.send_keys("1.9")

            trailing_stop_loss_el = wait.until(EC.element_to_be_clickable((By.ID, "trailingStoplossPriceModel")))
            trailing_stop_loss_el.clear()
            for _ in range(7):
                time.sleep(0.3)
                trailing_stop_loss_el.send_keys(Keys.ARROW_UP)

            # if not target_price_input_:
            #     test_results.append({
            #         "Page": "Order Window",
            #         "Testing_Area": "Target Price Input",
            #         "expected": "Target Price Input clicked",
            #         "actual": "Target Price Input clicked successfully",
            #         "status": "pass"
            #     })
            #     target_price_input_ = True

            # for _ in range(3):
            #     time.sleep(0.3)

            # Step 5: Select LONG TERM
            if cover_scenario["intraday"]:
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Intraday']"))
                ).click()
                print("✔ Selected Intraday")

            time.sleep(1)

            # Step 7: CLICK BUY
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Buy']"))
            ).click()
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Yes']"))
            ).click()
            print("🟢 BUY button clicked")

            time.sleep(3)

        print("\n🎉 All 4 scenarios executed successfully!")
        #
        for cover_scenario_sl in scenarios_cover_order_sl:
            print(f"\n===================== {cover_scenario_sl['tag']} =====================")
            common_fun()
            # Step 1: GET SCRIP AGAIN
            scrip_items = driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'border-b') and contains(@class, 'bgCardColor') and contains(@id, '|NSE')]"
            )

            if not scrip_items:
                print("❌ No scrip found in watchlist.")
                return

            scrip = scrip_items[0]
            driver.execute_script("arguments[0].scrollIntoView(true);", scrip)
            ActionChains(driver).move_to_element(scrip).perform()
            time.sleep(1)

            # Click BUY button
            buy_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='B']")
            buy_button.click()
            print("🟢 Order window opened")
            time.sleep(2)

            # Step 2: Click REGULAR
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='BO/CO']"))
            ).click()
            print("✔ Selected Cover")
            time.sleep(1)

            # Step 3: Click LIMIT
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='SL']"))
            ).click()
            print("✔ Selected Limit")
            time.sleep(1)

            # Step 5: Select LONG TERM
            if cover_scenario_sl["intraday"]:
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Intraday']"))
                ).click()
                print("✔ Selected Intraday")

            time.sleep(1)

            stop_loss_el = wait.until(EC.element_to_be_clickable((By.ID, "firstlegTriggerPrice")))
            stop_loss_el.clear()
            for _ in range(10):
                time.sleep(0.3)
                stop_loss_el.send_keys(Keys.ARROW_UP)

            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='pending_check']"))
            ).click()
            qty_el = wait.until(EC.element_to_be_clickable((By.ID, "targetPrice")))
            qty_el.clear()
            qty_el.send_keys("1.9")

            trailing_stop_loss_el = wait.until(EC.element_to_be_clickable((By.ID, "trailingStoplossPriceModel")))
            trailing_stop_loss_el.clear()
            for _ in range(7):
                time.sleep(0.3)
                trailing_stop_loss_el.send_keys(Keys.ARROW_UP)
            # Step 7: CLICK BUY
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Buy']"))
            ).click()
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Yes']]"))
            ).click()
            print("🟢 BUY button clicked")

            time.sleep(3)

        print("\n🎉 All 4 scenarios executed successfully!")

        for amo_order in scenarios:
            print(f"\n===================== {amo_order['tag']} =====================")

            # Step 1: GET SCRIP AGAIN
            scrip_items = driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'border-b') and contains(@class, 'bgCardColor') and contains(@id, '|NSE')]"
            )

            if not scrip_items:
                print("❌ No scrip found in watchlist.")
                return

            scrip = scrip_items[0]
            driver.execute_script("arguments[0].scrollIntoView(true);", scrip)
            ActionChains(driver).move_to_element(scrip).perform()
            time.sleep(1)

            # Click BUY button
            buy_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='B']")
            buy_button.click()
            print("🟢 Order window opened")
            time.sleep(2)

            # Step 2: Click REGULAR
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='AMO']"))
            ).click()
            if not amo_tab_:
                test_results.append({
                    "Page": "Order Window",
                    "Testing_Area": "AMO tab",
                    "expected": "AMO tab clicked",
                    "actual": "AMO tab clicked successfully",
                    "order_type": "Buy",
                    "status": "pass"
                })
                amo_tab_ = True
            print("✔ Selected Regular")
            time.sleep(1)

            # Step 3: Click LIMIT
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Limit']"))
            ).click()
            print("✔ Selected Limit")
            time.sleep(1)

            # Step 4: Click ADVANCED OPTIONS
            wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class,'cursor-pointer') and contains(text(),'Advanced Options')]")
                )
            ).click()
            print("✔ Advanced Options opened")
            time.sleep(1)

            # ioc = driver.find_element(By.XPATH, "//div[@role='radio' and @aria-label='IOC']")
            # ioc.click()

            # Step 5: Select LONG TERM
            if amo_order["longterm"]:
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Long Term']"))
                ).click()
                print("✔ Selected Long Term")
            else:
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Intraday']"))
                ).click()
                print("✔ Selected Intraday")
            time.sleep(1)

            # Step 6: Select DAY or IOC using our new function
            select_validity(amo_order["validity"])

            # Step 7: CLICK BUY
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Buy']"))
            ).click()
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Yes']]"))
            ).click()
            print("🟢 BUY button clicked")

            time.sleep(3)

        for sl_scenario in scenarios_sl:
            print(f"\n===================== {sl_scenario['tag']} =====================")

            # Step 1: GET SCRIP AGAIN
            scrip_items = driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'border-b') and contains(@class, 'bgCardColor') and contains(@id, '|NSE')]"
            )

            if not scrip_items:
                print("❌ No scrip found in watchlist.")
                return

            scrip = scrip_items[0]
            driver.execute_script("arguments[0].scrollIntoView(true);", scrip)
            ActionChains(driver).move_to_element(scrip).perform()
            time.sleep(1)

            # Click BUY button
            buy_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='B']")
            buy_button.click()
            print("🟢 Order window opened")
            time.sleep(2)

            # Step 2: Click REGULAR
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='AMO']"))
            ).click()
            print("✔ Selected Regular")
            time.sleep(1)

            # Step 3: Click LIMIT
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='SL']"))
            ).click()
            print("✔ Selected Limit")
            time.sleep(1)

            # Step 4: Click ADVANCED OPTIONS
            wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class,'cursor-pointer') and contains(text(),'Advanced Options')]")
                )
            ).click()
            print("✔ Advanced Options opened")
            time.sleep(1)

            # ioc = driver.find_element(By.XPATH, "//div[@role='radio' and @aria-label='IOC']")
            # ioc.click()

            # Step 5: Select LONG TERM
            if sl_scenario["longterm"]:
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Long Term']"))
                ).click()
                print("✔ Selected Long Term")
            else:
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Intraday']"))
                ).click()
                print("✔ Selected Intraday")
            time.sleep(1)

            # Step 6: Select DAY or IOC using our new function
            select_validity(sl_scenario["validity"])

            # Step 7: CLICK BUY
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Buy']"))
            ).click()
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Yes']]"))
            ).click()
            print("🟢 BUY button clicked")

            time.sleep(3)

        print("\n🎉 All 4 scenarios executed successfully!")

        for mtf_order in scenarios:
            print(f"\n===================== {mtf_order['tag']} =====================")
            # Step 1: GET SCRIP AGAIN
            scrip_items = driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'border-b') and contains(@class, 'bgCardColor') and contains(@id, '|NSE')]"
            )

            if not scrip_items:
                print("❌ No scrip found in watchlist.")
                return

            scrip = scrip_items[0]
            driver.execute_script("arguments[0].scrollIntoView(true);", scrip)
            ActionChains(driver).move_to_element(scrip).perform()
            time.sleep(1)

            # Click BUY button
            buy_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='B']")
            buy_button.click()
            print("🟢 Order window opened")
            time.sleep(2)

            # Step 2: Click REGULAR
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='MTF']"))
            ).click()
            if not mtf_tab_:
                test_results.append({
                    "Page": "Order Window",
                    "Testing_Area": "MTF tab",
                    "expected": "MTF tab clicked",
                    "actual": "MTF tab clicked successfully",
                    "order_type": "Buy",
                    "status": "pass"
                })
                mtf_tab_ = True
            print("✔ Selected Regular")
            time.sleep(1)

            # Step 3: Click LIMIT
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Limit']"))
            ).click()
            print("✔ Selected Limit")
            time.sleep(1)

            # Step 4: Click ADVANCED OPTIONS
            wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class,'cursor-pointer') and contains(text(),'Advanced Options')]")
                )
            ).click()
            print("✔ Advanced Options opened")
            time.sleep(1)

            # ioc = driver.find_element(By.XPATH, "//div[@role='radio' and @aria-label='IOC']")
            # ioc.click()

            # Step 5: Select LONG TERM
            if mtf_order["longterm"]:
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Long Term']"))
                ).click()
                print("✔ Selected Long Term")
            else:
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Intraday']"))
                ).click()
                print("✔ Selected Intraday")
            time.sleep(1)

            # Step 6: Select DAY or IOC using our new function
            select_validity(mtf_order["validity"])

            # Step 7: CLICK BUY
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Buy']"))
            ).click()
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Yes']]"))
            ).click()
            print("🟢 BUY button clicked")

            time.sleep(3)

        for sl_scenario in scenarios_sl:
            print(f"\n===================== {sl_scenario['tag']} =====================")
            common_fun()
            # Step 1: GET SCRIP AGAIN
            scrip_items = driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'border-b') and contains(@class, 'bgCardColor') and contains(@id, '|NSE')]"
            )

            if not scrip_items:
                print("❌ No scrip found in watchlist.")
                return

            scrip = scrip_items[0]
            driver.execute_script("arguments[0].scrollIntoView(true);", scrip)
            ActionChains(driver).move_to_element(scrip).perform()
            time.sleep(1)

            # Click BUY button
            buy_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='B']")
            buy_button.click()
            print("🟢 Order window opened")
            time.sleep(2)

            # Step 2: Click REGULAR
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='MTF']"))
            ).click()
            print("✔ Selected Regular")
            time.sleep(1)

            # Step 3: Click LIMIT
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='SL']"))
            ).click()
            print("✔ Selected Limit")
            time.sleep(1)

            # Step 4: Click ADVANCED OPTIONS
            wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class,'cursor-pointer') and contains(text(),'Advanced Options')]")
                )
            ).click()
            print("✔ Advanced Options opened")
            time.sleep(1)

            # ioc = driver.find_element(By.XPATH, "//div[@role='radio' and @aria-label='IOC']")
            # ioc.click()

            # Step 5: Select LONG TERM
            if sl_scenario["longterm"]:
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Long Term']"))
                ).click()
                print("✔ Selected Long Term")
            else:
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Intraday']"))
                ).click()
                print("✔ Selected Intraday")
            time.sleep(1)

            # Step 6: Select DAY or IOC using our new function
            select_validity(sl_scenario["validity"])

            # Step 7: CLICK BUY
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Buy']"))
            ).click()
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Yes']]"))
            ).click()
            print("🟢 BUY button clicked")

            time.sleep(3)

        print("\n🎉 All 4 scenarios executed successfully!")

    def orderWindow_Sell(self, test_results, expected="pass"):
        driver = self.driver
        wait = WebDriverWait(driver, 12)
        buy_logged = False
        regular_logg = False
        limit_ = False
        advance_options_ = False
        longterm_ = False
        intraday_ = False
        buy_btton_ = False
        stop_loss_ = False
        # cover_ = False
        pending_checkbox_ = False
        target_price_input_ = False
        amo_tab_ = False
        mtf_tab_ = False
        validity_flag = False

        # ===================== SCENARIOS =====================
        scenarios = [
            {
                "tag": "Scenario 1 → Regular + Limit + Intraday + Day",
                "product": "Intraday",
                "validity": "DAY",
                "longterm": False
            },
            {
                "tag": "Scenario 2 → Regular + Limit + Intraday + IOC",
                "product": "Intraday",
                "validity": "IOC",
                "longterm": False
            },
            {
                "tag": "Scenario 3 → Regular + Limit + LongTerm + Day",
                "product": "LongTerm",
                "validity": "DAY",
                "longterm": True
            },
            {
                "tag": "Scenario 4 → Regular + Limit + LongTerm + IOC",
                "product": "LongTerm",
                "validity": "IOC",
                "longterm": True
            }
        ]

        scenarios_sl = [
            {
                "tag": "Scenario 1 → Regular + SL + Intraday + Day",
                "product": "Intraday",
                "validity": "DAY",
                "longterm": False
            },
            {
                "tag": "Scenario 2 → Regular + SL + Intraday + IOC",
                "product": "Intraday",
                "validity": "IOC",
                "longterm": False
            },
            {
                "tag": "Scenario 3 → Regular + SL + LongTerm + Day",
                "product": "LongTerm",
                "validity": "DAY",
                "longterm": True
            },
            {
                "tag": "Scenario 4 → Regular + SL + LongTerm + IOC",
                "product": "LongTerm",
                "validity": "IOC",
                "longterm": True
            }
        ]

        scenarios_cover_order = [
            {
                "tag": "Scenario 1 → Cover + SL + Intraday + Day",
                "product": "Intraday",
                "intraday": True
            },
        ]
        scenarios_cover_order_sl = [
            {
                "tag": "Scenario 1 → Cover + SL + Intraday + Day",
                "product": "Intraday",
                "intraday": True
            },
        ]

        def common_fun():
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='Watchlist3']")))
            element.click()

        def append_result(test_results, page, area, expected, actual, status):
            test_results.append({
                "Page": page,
                "Testing_Area": area,
                "expected": expected,
                "actual": actual,
                "status": status
            })

        # ======================================================
        # FUNCTION → CLICK VALIDITY RADIO BUTTON
        # ======================================================

        def select_validity(validity):
            try:
                print(f"➡ Selecting Validity: {validity}")
                radio_xpath = f"//div[@role='radio' and @aria-label='{validity}']//div[contains(@class,'flex')]"

                option = wait.until(EC.element_to_be_clickable((By.XPATH, radio_xpath)))
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", option)
                driver.execute_script("arguments[0].click();", option)
                if validity not in self.logged_validities:
                    append_result(
                        test_results=test_results,
                        page="Order Window",
                        area=f"{validity} button",
                        expected=f"{validity} button clicked",
                        actual=f"{validity} button clicked successfully",
                        status="pass"
                    )
                    self.logged_validities.add(validity)
            except Exception as e:
                if validity not in self.logged_validities:
                    append_result(
                        test_results=test_results,
                        page="Order Window",
                        area=f"{validity} button",
                        expected=f"{validity} button clicked",
                        actual=str(e),
                        status="fail"
                    )

            print(f"✔ Selected {validity}")
            time.sleep(0.5)

        # ======================================================
        # MAIN LOOP FOR ALL SCENARIOS
        # ======================================================
        for scenario in scenarios:
            print(f"\n===================== {scenario['tag']} =====================")
            try:
                common_fun()
                # Step 1: GET SCRIP AGAIN
                scrip_items = driver.find_elements(
                    By.XPATH,
                    "//div[contains(@class, 'border-b') and contains(@class, 'bgCardColor') and contains(@id, '|NSE')]"
                )

                if not scrip_items:
                    print("❌ No scrip found in watchlist.")
                    return

                scrip = scrip_items[0]
                driver.execute_script("arguments[0].scrollIntoView(true);", scrip)
                ActionChains(driver).move_to_element(scrip).perform()
                time.sleep(1)

                # Click BUY button
                sell_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='S']")
                sell_button.click()
                print("🟢 Order window opened")
                if not buy_logged:
                    test_results.append({
                        "Page": "Order Window",
                        "Testing_Area": "Sell button",
                        "expected": "Sell button clicked",
                        "actual": "Sell button clicked successfully",
                        "order_type": "Sell",
                        "status": "pass"
                    })
                    buy_logged = True

                # Step 2: Click REGULAR
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Regular']"))
                ).click()
                print("✔ Selected Regular")
                if not regular_logg:
                    test_results.append({
                        "Page": "Order Window",
                        "Testing_Area": "Regular tab",
                        "expected": "Regular tab clicked",
                        "actual": "Regular tab clicked successfully",
                        "order_type": "Sell",
                        "status": "pass"
                    })
                    regular_logg = True
                time.sleep(1)

                # Step 3: Click LIMIT
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Limit']"))
                ).click()
                print("✔ Selected Limit")
                if not limit_:
                    test_results.append({
                        "Page": "Order Window",
                        "Testing_Area": "Limit tab",
                        "expected": "Limit tab clicked",
                        "actual": "Limit tab clicked successfully",
                        "order_type": "Sell",
                        "status": "pass"
                    })
                    limit_ = True
                time.sleep(1)

                # Step 4: Click ADVANCED OPTIONS
                wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//div[contains(@class,'cursor-pointer') and contains(text(),'Advanced Options')]")
                    )
                ).click()
                if not advance_options_:
                    test_results.append({
                        "Page": "Order Window",
                        "Testing_Area": "Advance option checkbox",
                        "expected": "Advance option checkbox clicked",
                        "actual": "Advance option checkbox clicked successfully",
                        "order_type": "Sell",
                        "status": "pass"
                    })
                    advance_options_ = True
                print("✔ Advanced Options opened")
                time.sleep(1)

                # ioc = driver.find_element(By.XPATH, "//div[@role='radio' and @aria-label='IOC']")
                # ioc.click()

                # Step 5: Select LONG TERM
                if scenario["longterm"]:
                    wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Long Term']"))
                    ).click()
                    if not longterm_:
                        test_results.append({
                            "Page": "Order Window",
                            "Testing_Area": "Longterm tab",
                            "expected": "Longterm tab clicked",
                            "actual": "Longterm tab clicked successfully",
                            "order_type": "Sell",
                            "status": "pass"
                        })
                        longterm_ = True

                    print("✔ Selected Long Term")
                else:
                    wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Intraday']"))
                    ).click()
                    if not intraday_:
                        test_results.append({
                            "Page": "Order Window",
                            "Testing_Area": "Intraday tab",
                            "expected": "Intraday tab clicked",
                            "actual": "Intraday tab clicked successfully",
                            "order_type": "Sell",
                            "status": "pass"
                        })
                        intraday_ = True
                    print("✔ Selected Intraday")
                time.sleep(1)

                # Step 6: Select DAY or IOC using our new function
                select_validity(scenario["validity"])

                try:
                    # Step 7: CLICK BUY
                    wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Sell']"))
                    ).click()
                    if not buy_btton_:
                        test_results.append({
                            "Page": "Order Window",
                            "Testing_Area": "Buy button",
                            "expected": "Buy button clicked",
                            "actual": "Buy button clicked and order placed successfully",
                            "order_type": "Sell",
                            "status": "pass"
                        })
                        buy_btton_ = True
                    print("🟢 BUY button clicked")
                except Exception as e:
                    if not buy_btton_:
                        test_results.append({
                            "Page": "Order Window",
                            "Testing_Area": "Buy button",
                            "expected": "Xpath not valid",
                            "actual": "Buy button clicked failed",
                            "order_type": "Sell",
                            "status": "fail"
                        })
                        buy_btton_ = True

                time.sleep(3)

                print("\n🎉 All 4 scenarios executed successfully!")

                time.sleep(3)
            except Exception as e:
                print(e)

        for sl_scenario in scenarios_sl:
            print(f"\n===================== {sl_scenario['tag']} =====================")
            common_fun()
            # Step 1: GET SCRIP AGAIN
            scrip_items = driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'border-b') and contains(@class, 'bgCardColor') and contains(@id, '|NSE')]"
            )

            if not scrip_items:
                print("❌ No scrip found in watchlist.")
                return

            scrip = scrip_items[0]
            driver.execute_script("arguments[0].scrollIntoView(true);", scrip)
            ActionChains(driver).move_to_element(scrip).perform()
            time.sleep(1)

            # Click BUY button
            buy_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='S']")
            buy_button.click()
            print("🟢 Order window opened")
            time.sleep(2)

            # Step 2: Click REGULAR
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Regular']"))
            ).click()
            print("✔ Selected Regular")
            time.sleep(1)

            # Step 3: Click LIMIT
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='SL']"))
            ).click()
            if not stop_loss_:
                test_results.append({
                    "Page": "Order Window",
                    "Testing_Area": "Stop loss tab",
                    "expected": "Stop loss tab clicked",
                    "actual": "Stop loss tab clicked successfully",
                    "order_type": "Sell",
                    "status": "pass"
                })
                stop_loss_ = True
            print("✔ Selected Limit")
            time.sleep(1)

            # Step 4: Click ADVANCED OPTIONS
            wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class,'cursor-pointer') and contains(text(),'Advanced Options')]")
                )
            ).click()
            print("✔ Advanced Options opened")
            time.sleep(1)

            # ioc = driver.find_element(By.XPATH, "//div[@role='radio' and @aria-label='IOC']")
            # ioc.click()

            # Step 5: Select LONG TERM
            if sl_scenario["longterm"]:
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Long Term']"))
                ).click()
                print("✔ Selected Long Term")
            else:
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Intraday']"))
                ).click()
                print("✔ Selected Intraday")
            time.sleep(1)

            # Step 6: Select DAY or IOC using our new function
            select_validity(sl_scenario["validity"])

            # Step 7: CLICK BUY
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Sell']"))
            ).click()
            print("🟢 BUY button clicked")

            time.sleep(3)

        print("\n🎉 All 4 scenarios executed successfully!")

        for cover_scenario in scenarios_cover_order:
            print(f"\n===================== {cover_scenario['tag']} =====================")
            common_fun()
            # Step 1: GET SCRIP AGAIN
            scrip_items = driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'border-b') and contains(@class, 'bgCardColor') and contains(@id, '|NSE')]"
            )

            if not scrip_items:
                print("❌ No scrip found in watchlist.")
                return

            scrip = scrip_items[0]
            driver.execute_script("arguments[0].scrollIntoView(true);", scrip)
            ActionChains(driver).move_to_element(scrip).perform()
            time.sleep(1)

            # Click BUY button
            buy_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='S']")
            buy_button.click()
            print("🟢 Order window opened")
            time.sleep(2)

            # Step 2: Click REGULAR
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='BO/CO']"))
            ).click()
            print("✔ Selected Cover")
            time.sleep(1)

            # Step 3: Click LIMIT
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Limit']"))
            ).click()
            print("✔ Selected Limit")
            time.sleep(1)

            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='pending_check']"))
            ).click()
            if not pending_checkbox_:
                test_results.append({
                    "Page": "Order Window",
                    "Testing_Area": "Pending checkbox",
                    "expected": "Pending checkbox clicked",
                    "actual": "Pending checkbox clicked successfully",
                    "order_type": "Sell",
                    "status": "pass"
                })
                pending_checkbox_ = True
            print("Target_button")
            time.sleep(1)

            stop_loss_el = wait.until(EC.element_to_be_clickable((By.ID, "firstlegTriggerPrice")))
            stop_loss_el.clear()
            for _ in range(10):
                time.sleep(0.3)
                stop_loss_el.send_keys(Keys.ARROW_UP)

            qty_el = wait.until(EC.element_to_be_clickable((By.ID, "targetPrice")))
            qty_el.clear()
            qty_el.send_keys("1.9")

            trailing_stop_loss_el = wait.until(EC.element_to_be_clickable((By.ID, "trailingStoplossPriceModel")))
            trailing_stop_loss_el.clear()
            for _ in range(7):
                time.sleep(0.3)
                trailing_stop_loss_el.send_keys(Keys.ARROW_UP)
            # if not target_price_input_:
            #     test_results.append({
            #         "Page": "Order Window",
            #         "Testing_Area": "Target Price Input",
            #         "expected": "Target Price Input clicked",
            #         "actual": "Target Price Input clicked successfully",
            #         "status": "pass"
            #     })
            #     target_price_input_ = True

            # for _ in range(3):
            #     time.sleep(0.3)

            # Step 5: Select LONG TERM
            if cover_scenario["intraday"]:
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Intraday']"))
                ).click()
                print("✔ Selected Intraday")

            time.sleep(1)

            # Step 7: CLICK BUY
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Sell']"))
            ).click()
            print("🟢 BUY button clicked")

            time.sleep(3)

        # print("\n🎉 All 4 scenarios executed successfully!")
        #
        for cover_scenario_sl in scenarios_cover_order_sl:
            print(f"\n===================== {cover_scenario_sl['tag']} =====================")
            common_fun()
            # Step 1: GET SCRIP AGAIN
            scrip_items = driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'border-b') and contains(@class, 'bgCardColor') and contains(@id, '|NSE')]"
            )

            if not scrip_items:
                print("❌ No scrip found in watchlist.")
                return

            scrip = scrip_items[0]
            driver.execute_script("arguments[0].scrollIntoView(true);", scrip)
            ActionChains(driver).move_to_element(scrip).perform()
            time.sleep(1)

            # Click BUY button
            buy_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='S']")
            buy_button.click()
            print("🟢 Order window opened")
            time.sleep(2)

            # Step 2: Click REGULAR
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='BO/CO']"))
            ).click()
            print("✔ Selected Cover")
            time.sleep(1)

            # Step 3: Click LIMIT
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='SL']"))
            ).click()
            print("✔ Selected Limit")
            time.sleep(1)

            # Step 5: Select LONG TERM
            if cover_scenario_sl["intraday"]:
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Intraday']"))
                ).click()
                print("✔ Selected Intraday")

            time.sleep(1)

            # Step 7: CLICK BUY
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Sell']"))
            ).click()
            print("🟢 BUY button clicked")

            time.sleep(3)

        print("\n🎉 All 4 scenarios executed successfully!")

        for amo_order in scenarios:
            print(f"\n===================== {amo_order['tag']} =====================")

            # Step 1: GET SCRIP AGAIN
            scrip_items = driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'border-b') and contains(@class, 'bgCardColor') and contains(@id, '|NSE')]"
            )

            if not scrip_items:
                print("❌ No scrip found in watchlist.")
                return

            scrip = scrip_items[0]
            driver.execute_script("arguments[0].scrollIntoView(true);", scrip)
            ActionChains(driver).move_to_element(scrip).perform()
            time.sleep(1)

            # Click BUY button
            buy_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='S']")
            buy_button.click()
            print("🟢 Order window opened")
            time.sleep(2)

            # Step 2: Click REGULAR
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='AMO']"))
            ).click()
            if not amo_tab_:
                test_results.append({
                    "Page": "Order Window",
                    "Testing_Area": "AMO tab",
                    "expected": "AMO tab clicked",
                    "actual": "AMO tab clicked successfully",
                    "order_type": "Sell",
                    "status": "pass"
                })
                amo_tab_ = True
            print("✔ Selected Regular")
            time.sleep(1)

            # Step 3: Click LIMIT
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Limit']"))
            ).click()
            print("✔ Selected Limit")
            time.sleep(1)

            # Step 4: Click ADVANCED OPTIONS
            wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class,'cursor-pointer') and contains(text(),'Advanced Options')]")
                )
            ).click()
            print("✔ Advanced Options opened")
            time.sleep(1)

            # ioc = driver.find_element(By.XPATH, "//div[@role='radio' and @aria-label='IOC']")
            # ioc.click()

            # Step 5: Select LONG TERM
            if amo_order["longterm"]:
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Long Term']"))
                ).click()
                print("✔ Selected Long Term")
            else:
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Intraday']"))
                ).click()
                print("✔ Selected Intraday")
            time.sleep(1)

            # Step 6: Select DAY or IOC using our new function
            select_validity(amo_order["validity"])

            # Step 7: CLICK BUY
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Sell']"))
            ).click()
            print("🟢 BUY button clicked")

            time.sleep(3)

        for sl_scenario in scenarios_sl:
            print(f"\n===================== {sl_scenario['tag']} =====================")

            # Step 1: GET SCRIP AGAIN
            scrip_items = driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'border-b') and contains(@class, 'bgCardColor') and contains(@id, '|NSE')]"
            )

            if not scrip_items:
                print("❌ No scrip found in watchlist.")
                return

            scrip = scrip_items[0]
            driver.execute_script("arguments[0].scrollIntoView(true);", scrip)
            ActionChains(driver).move_to_element(scrip).perform()
            time.sleep(1)

            # Click BUY button
            buy_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='S']")
            buy_button.click()
            print("🟢 Order window opened")
            time.sleep(2)

            # Step 2: Click REGULAR
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='AMO']"))
            ).click()
            print("✔ Selected Regular")
            time.sleep(1)

            # Step 3: Click LIMIT
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='SL']"))
            ).click()
            print("✔ Selected Limit")
            time.sleep(1)

            # Step 4: Click ADVANCED OPTIONS
            wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class,'cursor-pointer') and contains(text(),'Advanced Options')]")
                )
            ).click()
            print("✔ Advanced Options opened")
            time.sleep(1)

            # ioc = driver.find_element(By.XPATH, "//div[@role='radio' and @aria-label='IOC']")
            # ioc.click()

            # Step 5: Select LONG TERM
            if sl_scenario["longterm"]:
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Long Term']"))
                ).click()
                print("✔ Selected Long Term")
            else:
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Intraday']"))
                ).click()
                print("✔ Selected Intraday")
            time.sleep(1)

            # Step 6: Select DAY or IOC using our new function
            select_validity(sl_scenario["validity"])

            # Step 7: CLICK BUY
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Sell']"))
            ).click()
            print("🟢 BUY button clicked")

            time.sleep(3)

        print("\n🎉 All 4 scenarios executed successfully!")

        for mtf_order in scenarios:
            print(f"\n===================== {mtf_order['tag']} =====================")
            # Step 1: GET SCRIP AGAIN
            scrip_items = driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'border-b') and contains(@class, 'bgCardColor') and contains(@id, '|NSE')]"
            )

            if not scrip_items:
                print("❌ No scrip found in watchlist.")
                return

            scrip = scrip_items[0]
            driver.execute_script("arguments[0].scrollIntoView(true);", scrip)
            ActionChains(driver).move_to_element(scrip).perform()
            time.sleep(1)

            # Click BUY button
            buy_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='S']")
            buy_button.click()
            print("🟢 Order window opened")
            time.sleep(2)

            # Step 2: Click REGULAR
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='MTF']"))
            ).click()
            if not mtf_tab_:
                test_results.append({
                    "Page": "Order Window",
                    "Testing_Area": "MTF tab",
                    "expected": "MTF tab clicked",
                    "actual": "MTF tab clicked successfully",
                    "order_type": "Sell",
                    "status": "pass"
                })
                mtf_tab_ = True
            print("✔ Selected Regular")
            time.sleep(1)

            # Step 3: Click LIMIT
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Limit']"))
            ).click()
            print("✔ Selected Limit")
            time.sleep(1)

            # Step 4: Click ADVANCED OPTIONS
            wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class,'cursor-pointer') and contains(text(),'Advanced Options')]")
                )
            ).click()
            print("✔ Advanced Options opened")
            time.sleep(1)

            # ioc = driver.find_element(By.XPATH, "//div[@role='radio' and @aria-label='IOC']")
            # ioc.click()

            # Step 5: Select LONG TERM
            if mtf_order["longterm"]:
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Long Term']"))
                ).click()
                print("✔ Selected Long Term")
            else:
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Intraday']"))
                ).click()
                print("✔ Selected Intraday")
            time.sleep(1)

            # Step 6: Select DAY or IOC using our new function
            select_validity(mtf_order["validity"])

            # Step 7: CLICK BUY
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Sell']"))
            ).click()
            print("🟢 BUY button clicked")

            time.sleep(3)
        #
        for sl_scenario in scenarios_sl:
            print(f"\n===================== {sl_scenario['tag']} =====================")
            common_fun()
            # Step 1: GET SCRIP AGAIN
            scrip_items = driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'border-b') and contains(@class, 'bgCardColor') and contains(@id, '|NSE')]"
            )

            if not scrip_items:
                print("❌ No scrip found in watchlist.")
                return

            scrip = scrip_items[0]
            driver.execute_script("arguments[0].scrollIntoView(true);", scrip)
            ActionChains(driver).move_to_element(scrip).perform()
            time.sleep(1)

            # Click BUY button
            buy_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='S']")
            buy_button.click()
            print("🟢 Order window opened")
            time.sleep(2)

            # Step 2: Click REGULAR
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='MTF']"))
            ).click()
            print("✔ Selected Regular")
            time.sleep(1)

            # Step 3: Click LIMIT
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='SL']"))
            ).click()
            print("✔ Selected Limit")
            time.sleep(1)

            # Step 4: Click ADVANCED OPTIONS
            wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class,'cursor-pointer') and contains(text(),'Advanced Options')]")
                )
            ).click()
            print("✔ Advanced Options opened")
            time.sleep(1)

            # ioc = driver.find_element(By.XPATH, "//div[@role='radio' and @aria-label='IOC']")
            # ioc.click()

            # Step 5: Select LONG TERM
            if sl_scenario["longterm"]:
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Long Term']"))
                ).click()
                print("✔ Selected Long Term")
            else:
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Intraday']"))
                ).click()
                print("✔ Selected Intraday")
            time.sleep(1)

            # Step 6: Select DAY or IOC using our new function
            select_validity(sl_scenario["validity"])

            # Step 7: CLICK BUY
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Sell']"))
            ).click()
            print("🟢 BUY button clicked")

            time.sleep(3)

        print("\n🎉 All 4 scenarios executed successfully!")

    # def orderWindow_Sell(self, test_results, expected="pass"):
    #     driver = self.driver
    #     wait = WebDriverWait(driver, 12)
    #
    #     if not hasattr(self, "logged_validities"):
    #         self.logged_validities = set()
    #
    #     # ===================== SCENARIOS =====================
    #     scenarios = [
    #         {
    #             "tag": "Scenario 1 → Regular + Limit + Intraday + Day",
    #             "product": "Intraday",
    #             "validity": "DAY",
    #             "longterm": False
    #         },
    #         {
    #             "tag": "Scenario 2 → Regular + Limit + Intraday + IOC",
    #             "product": "Intraday",
    #             "validity": "IOC",
    #             "longterm": False
    #         },
    #         {
    #             "tag": "Scenario 3 → Regular + Limit + LongTerm + Day",
    #             "product": "LongTerm",
    #             "validity": "DAY",
    #             "longterm": True
    #         },
    #         {
    #             "tag": "Scenario 4 → Regular + Limit + LongTerm + IOC",
    #             "product": "LongTerm",
    #             "validity": "IOC",
    #             "longterm": True
    #         }
    #     ]
    #
    #     scenarios_sl = [
    #         {
    #             "tag": "Scenario 1 → Regular + SL + Intraday + Day",
    #             "product": "Intraday",
    #             "validity": "DAY",
    #             "longterm": False
    #         },
    #         {
    #             "tag": "Scenario 2 → Regular + SL + Intraday + IOC",
    #             "product": "Intraday",
    #             "validity": "IOC",
    #             "longterm": False
    #         },
    #         {
    #             "tag": "Scenario 3 → Regular + SL + LongTerm + Day",
    #             "product": "LongTerm",
    #             "validity": "DAY",
    #             "longterm": True
    #         },
    #         {
    #             "tag": "Scenario 4 → Regular + SL + LongTerm + IOC",
    #             "product": "LongTerm",
    #             "validity": "IOC",
    #             "longterm": True
    #         }
    #     ]
    #
    #     scenarios_cover_order = [
    #         {
    #             "tag": "Scenario 1 → Cover + SL + Intraday + Day",
    #             "product": "Intraday",
    #             "intraday": True
    #         },
    #     ]
    #     scenarios_cover_order_sl = [
    #         {
    #             "tag": "Scenario 1 → Cover + SL + Intraday + Day",
    #             "product": "Intraday",
    #             "intraday": True
    #         },
    #     ]
    #
    #     def common_fun():
    #         element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='Watchlist1']")))
    #         element.click()
    #
    #     def append_result(test_results, page, area, expected, actual, status):
    #         test_results.append({
    #             "Page": page,
    #             "Testing_Area": area,
    #             "expected": expected,
    #             "actual": actual,
    #             "status": status
    #         })
    #
    #     # ======================================================
    #     # FUNCTION → CLICK VALIDITY RADIO BUTTON
    #     # ======================================================
    #     def select_validity(validity):
    #         try:
    #             print(f"➡ Selecting Validity: {validity}")
    #
    #             radio_xpath = (
    #                 f"//div[@role='radio' and @aria-label='{validity}']"
    #                 "//div[contains(@class,'flex')]"
    #             )
    #
    #             option = wait.until(EC.element_to_be_clickable((By.XPATH, radio_xpath)))
    #             driver.execute_script(
    #                 "arguments[0].scrollIntoView({block:'center'});", option
    #             )
    #             driver.execute_script("arguments[0].click();", option)
    #
    #             # ✅ LOG ONLY ONCE
    #             if validity not in self.logged_validities:
    #                 append_result(
    #                     test_results=test_results,
    #                     page="Order Window",
    #                     area=f"{validity} button",
    #                     expected=f"{validity} button clicked",
    #                     actual=f"{validity} button clicked successfully",
    #                     status="pass"
    #                 )
    #                 self.logged_validities.add(validity)
    #
    #         except Exception as e:
    #             if validity not in self.logged_validities:
    #                 append_result(
    #                     test_results=test_results,
    #                     page="Order Window",
    #                     area=f"{validity} button",
    #                     expected=f"{validity} button clicked",
    #                     actual=str(e),
    #                     status="fail"
    #                 )
    #                 self.logged_validities.add(validity)
    #
    #     # ======================================================
    #     # MAIN LOOP FOR ALL SCENARIOS
    #     # ======================================================
    #     for scenario in scenarios:
    #         print(f"\n===================== {scenario['tag']} =====================")
    #
    #         common_fun()
    #         # Step 1: GET SCRIP AGAIN
    #         scrip_items = driver.find_elements(
    #             By.XPATH,
    #             "//div[contains(@class, 'border-b') and contains(@class, 'bgCardColor') and contains(@id, '|NSE')]"
    #         )
    #
    #         if not scrip_items:
    #             print("❌ No scrip found in watchlist.")
    #             return
    #
    #         scrip = scrip_items[0]
    #         driver.execute_script("arguments[0].scrollIntoView(true);", scrip)
    #         ActionChains(driver).move_to_element(scrip).perform()
    #         time.sleep(1)
    #
    #         # Click BUY button
    #         sell_button = scrip.find_element(By.XPATH, "//button[normalize-space()='S']")
    #         sell_button.click()
    #         print("🟢 Order window opened")
    #         # if not sell_logged_:
    #         #     test_results.append({
    #         #         "Page": "Order Window",
    #         #         "Testing_Area": "Buy button",
    #         #         "expected": "Buy button clicked",
    #         #         "actual": "Buy button clicked successfully",
    #         #         "order_type": "Sell",
    #         #         "status": "pass"
    #         #     })
    #         #     sell_logged_ = True
    #
    #         time.sleep(2)
    #
    #         # Step 2: Click REGULAR
    #         wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Regular']"))
    #         ).click()
    #         # if not regular_logg_sell:
    #         #     test_results.append({
    #         #         "Page": "Order Window",
    #         #         "Testing_Area": "Regular tab",
    #         #         "expected": "Regular tab clicked",
    #         #         "actual": "Regular tab clicked successfully",
    #         #         "order_type": "Sell",
    #         #         "status": "pass"
    #         #     })
    #         #     regular_logg_sell = True
    #         print("✔ Selected Regular")
    #         time.sleep(1)
    #
    #         # Step 3: Click LIMIT
    #         wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Limit']"))
    #         ).click()
    #         # if not limit_sell:
    #         #     test_results.append({
    #         #         "Page": "Order Window",
    #         #         "Testing_Area": "Limit tab",
    #         #         "expected": "Limit tab clicked",
    #         #         "actual": "Limit tab clicked successfully",
    #         #         "order_type": "Sell",
    #         #         "status": "pass"
    #         #     })
    #         #     limit_sell = True
    #         print("✔ Selected Limit")
    #         time.sleep(1)
    #
    #         # Step 4: Click ADVANCED OPTIONS
    #         wait.until(
    #             EC.element_to_be_clickable(
    #                 (By.XPATH, "//div[contains(@class,'cursor-pointer') and contains(text(),'Advanced Options')]")
    #             )
    #         ).click()
    #         # if not advance_options_sell:
    #         #     test_results.append({
    #         #         "Page": "Order Window",
    #         #         "Testing_Area": "Advance option checkbox",
    #         #         "expected": "Advance option checkbox clicked",
    #         #         "actual": "Advance option checkbox clicked successfully",
    #         #         "order_type": "Sell",
    #         #         "status": "pass"
    #         #     })
    #         #     advance_options_sell = True
    #         print("✔ Advanced Options opened")
    #         time.sleep(1)
    #
    #         # ioc = driver.find_element(By.XPATH, "//div[@role='radio' and @aria-label='IOC']")
    #         # ioc.click()
    #
    #         # Step 5: Select LONG TERM
    #         if scenario["longterm"]:
    #             wait.until(
    #                 EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Long Term']"))
    #             ).click()
    #             # if not longterm_sell:
    #             #     test_results.append({
    #             #         "Page": "Order Window",
    #             #         "Testing_Area": "Longterm tab",
    #             #         "expected": "Longterm tab clicked",
    #             #         "actual": "Longterm tab clicked successfully",
    #             #         "order_type": "Sell",
    #             #         "status": "pass"
    #             #     })
    #             #     longterm_sell = True
    #             print("✔ Selected Long Term")
    #         else:
    #             wait.until(
    #                 EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Intraday']"))
    #             ).click()
    #             # if not intraday_sell:
    #             #     test_results.append({
    #             #         "Page": "Order Window",
    #             #         "Testing_Area": "Intraday tab",
    #             #         "expected": "Intraday tab clicked",
    #             #         "actual": "Intraday tab clicked successfully",
    #             #         "order_type": "Sell",
    #             #         "status": "pass"
    #             #     })
    #             #     intraday_sell = True
    #             print("✔ Selected Intraday")
    #         time.sleep(1)
    #
    #         # Step 6: Select DAY or IOC using our new function
    #         select_validity(scenario["validity"])
    #
    #         # Step 7: CLICK BUY
    #         wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Sell']"))
    #         ).click()
    #         if not buy_btton_sell:
    #             test_results.append({
    #                 "Page": "Order Window",
    #                 "Testing_Area": "Sell button",
    #                 "expected": "Sell button clicked",
    #                 "actual": "Sell button clicked successfully",
    #                 "order_type": "Sell",
    #                 "status": "pass"
    #             })
    #             buy_btton_sell = True
    #         print("🟢 BUY button clicked")
    #
    #         time.sleep(3)
    #
    #     print("\n🎉 All 4 scenarios executed successfully!")
    #
    #     time.sleep(3)
    #
    #     for sl_scenario in scenarios_sl:
    #         print(f"\n===================== {sl_scenario['tag']} =====================")
    #         common_fun()
    #         # Step 1: GET SCRIP AGAIN
    #         scrip_items = driver.find_elements(
    #             By.XPATH,
    #             "//div[contains(@class, 'border-b') and contains(@class, 'bgCardColor') and contains(@id, '|NSE')]"
    #         )
    #
    #         if not scrip_items:
    #             print("❌ No scrip found in watchlist.")
    #             return
    #
    #         scrip = scrip_items[0]
    #         driver.execute_script("arguments[0].scrollIntoView(true);", scrip)
    #         ActionChains(driver).move_to_element(scrip).perform()
    #         time.sleep(1)
    #
    #         # Click BUY button
    #         buy_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='S']")
    #         buy_button.click()
    #         print("🟢 Order window opened")
    #         time.sleep(2)
    #
    #         # Step 2: Click REGULAR
    #         wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Regular']"))
    #         ).click()
    #         print("✔ Selected Regular")
    #         time.sleep(1)
    #
    #         # Step 3: Click LIMIT
    #         wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='SL']"))
    #         ).click()
    #         # if not stop_loss_sell:
    #         #     test_results.append({
    #         #         "Page": "Order Window",
    #         #         "Testing_Area": "Stop loss tab",
    #         #         "expected": "Stop loss tab clicked",
    #         #         "actual": "Stop loss tab clicked successfully",
    #         #         "order_type": "Sell",
    #         #         "status": "pass"
    #         #     })
    #         #     stop_loss_sell = True
    #         print("✔ Selected Limit")
    #         time.sleep(1)
    #
    #         # Step 4: Click ADVANCED OPTIONS
    #         wait.until(
    #             EC.element_to_be_clickable(
    #                 (By.XPATH, "//div[contains(@class,'cursor-pointer') and contains(text(),'Advanced Options')]")
    #             )
    #         ).click()
    #         # if not pending_checkbox_sell:
    #         #     test_results.append({
    #         #         "Page": "Order Window",
    #         #         "Testing_Area": "Pending checkbox",
    #         #         "expected": "Pending checkbox clicked",
    #         #         "actual": "Pending checkbox clicked successfully",
    #         #         "order_type": "Sell",
    #         #         "status": "pass"
    #         #     })
    #         #     pending_checkbox_sell = True
    #         print("✔ Advanced Options opened")
    #         time.sleep(1)
    #
    #         # ioc = driver.find_element(By.XPATH, "//div[@role='radio' and @aria-label='IOC']")
    #         # ioc.click()
    #
    #         # Step 5: Select LONG TERM
    #         if sl_scenario["longterm"]:
    #             wait.until(
    #                 EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Long Term']"))
    #             ).click()
    #             print("✔ Selected Long Term")
    #         else:
    #             wait.until(
    #                 EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Intraday']"))
    #             ).click()
    #             print("✔ Selected Intraday")
    #         time.sleep(1)
    #
    #         # Step 6: Select DAY or IOC using our new function
    #         select_validity(sl_scenario["validity"])
    #
    #         # Step 7: CLICK BUY
    #         wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Sell']"))
    #         ).click()
    #         print("🟢 BUY button clicked")
    #
    #         time.sleep(3)
    #
    #     print("\n🎉 All 4 scenarios executed successfully!")
    #
    #     for cover_scenario in scenarios_cover_order:
    #         print(f"\n===================== {cover_scenario['tag']} =====================")
    #         common_fun()
    #         # Step 1: GET SCRIP AGAIN
    #         scrip_items = driver.find_elements(
    #             By.XPATH,
    #             "//div[contains(@class, 'border-b') and contains(@class, 'bgCardColor') and contains(@id, '|NSE')]"
    #         )
    #
    #         if not scrip_items:
    #             print("❌ No scrip found in watchlist.")
    #             return
    #
    #         scrip = scrip_items[0]
    #         driver.execute_script("arguments[0].scrollIntoView(true);", scrip)
    #         ActionChains(driver).move_to_element(scrip).perform()
    #         time.sleep(1)
    #
    #         # Click BUY button
    #         buy_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='S']")
    #         buy_button.click()
    #         print("🟢 Order window opened")
    #         time.sleep(2)
    #
    #         # Step 2: Click REGULAR
    #         wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Cover']"))
    #         ).click()
    #         print("✔ Selected Cover")
    #         time.sleep(1)
    #
    #         # Step 3: Click LIMIT
    #         wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Limit']"))
    #         ).click()
    #         print("✔ Selected Limit")
    #         time.sleep(1)
    #
    #         # Step 5: Select LONG TERM
    #         if cover_scenario["intraday"]:
    #             wait.until(
    #                 EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Intraday']"))
    #             ).click()
    #             print("✔ Selected Intraday")
    #
    #         time.sleep(1)
    #
    #         # Step 7: CLICK BUY
    #         wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Sell']"))
    #         ).click()
    #         print("🟢 BUY button clicked")
    #
    #         time.sleep(3)
    #
    #     print("\n🎉 All 4 scenarios executed successfully!")
    #
    #     for cover_scenario_sl in scenarios_cover_order_sl:
    #         print(f"\n===================== {cover_scenario_sl['tag']} =====================")
    #         common_fun()
    #         # Step 1: GET SCRIP AGAIN
    #         scrip_items = driver.find_elements(
    #             By.XPATH,
    #             "//div[contains(@class, 'border-b') and contains(@class, 'bgCardColor') and contains(@id, '|NSE')]"
    #         )
    #
    #         if not scrip_items:
    #             print("❌ No scrip found in watchlist.")
    #             return
    #
    #         scrip = scrip_items[0]
    #         driver.execute_script("arguments[0].scrollIntoView(true);", scrip)
    #         ActionChains(driver).move_to_element(scrip).perform()
    #         time.sleep(1)
    #
    #         # Click BUY button
    #         buy_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='S']")
    #         buy_button.click()
    #         print("🟢 Order window opened")
    #         time.sleep(2)
    #
    #         # Step 2: Click REGULAR
    #         wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Cover']"))
    #         ).click()
    #         print("✔ Selected Cover")
    #         time.sleep(1)
    #
    #         # Step 3: Click LIMIT
    #         wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='SL']"))
    #         ).click()
    #         print("✔ Selected Limit")
    #         time.sleep(1)
    #
    #         # Step 5: Select LONG TERM
    #         if cover_scenario_sl["intraday"]:
    #             wait.until(
    #                 EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Intraday']"))
    #             ).click()
    #             print("✔ Selected Intraday")
    #
    #         time.sleep(1)
    #
    #         # Step 7: CLICK BUY
    #         wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Sell']"))
    #         ).click()
    #         print("🟢 BUY button clicked")
    #
    #         time.sleep(3)
    #
    #     print("\n🎉 All 4 scenarios executed successfully!")
    #
    #     for amo_order in scenarios:
    #         print(f"\n===================== {amo_order['tag']} =====================")
    #
    #         # Step 1: GET SCRIP AGAIN
    #         scrip_items = driver.find_elements(
    #             By.XPATH,
    #             "//div[contains(@class, 'border-b') and contains(@class, 'bgCardColor') and contains(@id, '|NSE')]"
    #         )
    #
    #         if not scrip_items:
    #             print("❌ No scrip found in watchlist.")
    #             return
    #
    #         scrip = scrip_items[0]
    #         driver.execute_script("arguments[0].scrollIntoView(true);", scrip)
    #         ActionChains(driver).move_to_element(scrip).perform()
    #         time.sleep(1)
    #
    #         # Click BUY button
    #         buy_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='S']")
    #         buy_button.click()
    #         print("🟢 Order window opened")
    #         time.sleep(2)
    #
    #         # Step 2: Click REGULAR
    #         wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='AMO']"))
    #         ).click()
    #         # if not amo_tab_sell:
    #         #     test_results.append({
    #         #         "Page": "Order Window",
    #         #         "Testing_Area": "AMO tab",
    #         #         "expected": "AMO tab clicked",
    #         #         "actual": "AMO tab clicked successfully",
    #         #         "order_type": "Sell",
    #         #         "status": "pass"
    #         #     })
    #         #     amo_tab_sell = True
    #         print("✔ Selected Regular")
    #         time.sleep(1)
    #
    #         # Step 3: Click LIMIT
    #         wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Limit']"))
    #         ).click()
    #         print("✔ Selected Limit")
    #         time.sleep(1)
    #
    #         # Step 4: Click ADVANCED OPTIONS
    #         wait.until(
    #             EC.element_to_be_clickable(
    #                 (By.XPATH, "//div[contains(@class,'cursor-pointer') and contains(text(),'Advanced Options')]")
    #             )
    #         ).click()
    #         print("✔ Advanced Options opened")
    #         time.sleep(1)
    #
    #         # ioc = driver.find_element(By.XPATH, "//div[@role='radio' and @aria-label='IOC']")
    #         # ioc.click()
    #
    #         # Step 5: Select LONG TERM
    #         if amo_order["longterm"]:
    #             wait.until(
    #                 EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Long Term']"))
    #             ).click()
    #             print("✔ Selected Long Term")
    #         else:
    #             wait.until(
    #                 EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Intraday']"))
    #             ).click()
    #             print("✔ Selected Intraday")
    #         time.sleep(1)
    #
    #         # Step 6: Select DAY or IOC using our new function
    #         select_validity(amo_order["validity"])
    #
    #         # Step 7: CLICK BUY
    #         wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Sell']"))
    #         ).click()
    #         print("🟢 BUY button clicked")
    #
    #         time.sleep(3)
    #
    #     for sl_scenario in scenarios_sl:
    #         print(f"\n===================== {sl_scenario['tag']} =====================")
    #
    #         # Step 1: GET SCRIP AGAIN
    #         scrip_items = driver.find_elements(
    #             By.XPATH,
    #             "//div[contains(@class, 'border-b') and contains(@class, 'bgCardColor') and contains(@id, '|NSE')]"
    #         )
    #
    #         if not scrip_items:
    #             print("❌ No scrip found in watchlist.")
    #             return
    #
    #         scrip = scrip_items[0]
    #         driver.execute_script("arguments[0].scrollIntoView(true);", scrip)
    #         ActionChains(driver).move_to_element(scrip).perform()
    #         time.sleep(1)
    #
    #         # Click BUY button
    #         buy_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='S']")
    #         buy_button.click()
    #         print("🟢 Order window opened")
    #         time.sleep(2)
    #
    #         # Step 2: Click REGULAR
    #         wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='AMO']"))
    #         ).click()
    #         print("✔ Selected Regular")
    #         time.sleep(1)
    #
    #         # Step 3: Click LIMIT
    #         wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='SL']"))
    #         ).click()
    #         print("✔ Selected Limit")
    #         time.sleep(1)
    #
    #         # Step 4: Click ADVANCED OPTIONS
    #         wait.until(
    #             EC.element_to_be_clickable(
    #                 (By.XPATH, "//div[contains(@class,'cursor-pointer') and contains(text(),'Advanced Options')]")
    #             )
    #         ).click()
    #         print("✔ Advanced Options opened")
    #         time.sleep(1)
    #
    #         # ioc = driver.find_element(By.XPATH, "//div[@role='radio' and @aria-label='IOC']")
    #         # ioc.click()
    #
    #         # Step 5: Select LONG TERM
    #         if sl_scenario["longterm"]:
    #             wait.until(
    #                 EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Long Term']"))
    #             ).click()
    #             print("✔ Selected Long Term")
    #         else:
    #             wait.until(
    #                 EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Intraday']"))
    #             ).click()
    #             print("✔ Selected Intraday")
    #         time.sleep(1)
    #
    #         # Step 6: Select DAY or IOC using our new function
    #         select_validity(sl_scenario["validity"])
    #
    #         # Step 7: CLICK BUY
    #         wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Sell']"))
    #         ).click()
    #         print("🟢 BUY button clicked")
    #
    #         time.sleep(3)
    #
    #     print("\n🎉 All 4 scenarios executed successfully!")
    #
    #     for mtf_order in scenarios:
    #         print(f"\n===================== {mtf_order['tag']} =====================")
    #         # Step 1: GET SCRIP AGAIN
    #         scrip_items = driver.find_elements(
    #             By.XPATH,
    #             "//div[contains(@class, 'border-b') and contains(@class, 'bgCardColor') and contains(@id, '|NSE')]"
    #         )
    #
    #         if not scrip_items:
    #             print("❌ No scrip found in watchlist.")
    #             return
    #
    #         scrip = scrip_items[0]
    #         driver.execute_script("arguments[0].scrollIntoView(true);", scrip)
    #         ActionChains(driver).move_to_element(scrip).perform()
    #         time.sleep(1)
    #
    #         # Click BUY button
    #         buy_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='S']")
    #         buy_button.click()
    #         print("🟢 Order window opened")
    #         time.sleep(2)
    #
    #         # Step 2: Click REGULAR
    #         wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='MTF']"))
    #         ).click()
    #         print("✔ Selected Regular")
    #         time.sleep(1)
    #
    #         # Step 3: Click LIMIT
    #         wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Limit']"))
    #         ).click()
    #         print("✔ Selected Limit")
    #         time.sleep(1)
    #
    #         # Step 4: Click ADVANCED OPTIONS
    #         wait.until(
    #             EC.element_to_be_clickable(
    #                 (By.XPATH, "//div[contains(@class,'cursor-pointer') and contains(text(),'Advanced Options')]")
    #             )
    #         ).click()
    #         print("✔ Advanced Options opened")
    #         time.sleep(1)
    #
    #         # ioc = driver.find_element(By.XPATH, "//div[@role='radio' and @aria-label='IOC']")
    #         # ioc.click()
    #
    #         # Step 5: Select LONG TERM
    #         if mtf_order["longterm"]:
    #             wait.until(
    #                 EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Long Term']"))
    #             ).click()
    #             print("✔ Selected Long Term")
    #         else:
    #             wait.until(
    #                 EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Intraday']"))
    #             ).click()
    #             print("✔ Selected Intraday")
    #         time.sleep(1)
    #
    #         # Step 6: Select DAY or IOC using our new function
    #         select_validity(mtf_order["validity"])
    #
    #         # Step 7: CLICK BUY
    #         wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Sell']"))
    #         ).click()
    #         print("🟢 BUY button clicked")
    #
    #         time.sleep(3)
    #
    #     for sl_scenario in scenarios_sl:
    #         print(f"\n===================== {sl_scenario['tag']} =====================")
    #         common_fun()
    #         # Step 1: GET SCRIP AGAIN
    #         scrip_items = driver.find_elements(
    #             By.XPATH,
    #             "//div[contains(@class, 'border-b') and contains(@class, 'bgCardColor') and contains(@id, '|NSE')]"
    #         )
    #
    #         if not scrip_items:
    #             print("❌ No scrip found in watchlist.")
    #             return
    #
    #         scrip = scrip_items[0]
    #         driver.execute_script("arguments[0].scrollIntoView(true);", scrip)
    #         ActionChains(driver).move_to_element(scrip).perform()
    #         time.sleep(1)
    #
    #         # Click BUY button
    #         buy_button = scrip.find_element(By.XPATH, ".//button[normalize-space()='S']")
    #         buy_button.click()
    #         print("🟢 Order window opened")
    #         time.sleep(2)
    #
    #         # Step 2: Click REGULAR
    #         wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='MTF']"))
    #         ).click()
    #         print("✔ Selected Regular")
    #         time.sleep(1)
    #
    #         # Step 3: Click LIMIT
    #         wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='SL']"))
    #         ).click()
    #         # if not mtf_tab_sell:
    #         #     test_results.append({
    #         #         "Page": "Order Window",
    #         #         "Testing_Area": "MTF tab",
    #         #         "expected": "MTF tab clicked",
    #         #         "actual": "MTF tab clicked successfully",
    #         #         "order_type": "Sell",
    #         #         "status": "pass"
    #         #     })
    #         #     mtf_tab_sell = True
    #         print("✔ Selected Limit")
    #         time.sleep(1)
    #
    #         # Step 4: Click ADVANCED OPTIONS
    #         wait.until(
    #             EC.element_to_be_clickable(
    #                 (By.XPATH, "//div[contains(@class,'cursor-pointer') and contains(text(),'Advanced Options')]")
    #             )
    #         ).click()
    #         print("✔ Advanced Options opened")
    #         time.sleep(1)
    #
    #         # ioc = driver.find_element(By.XPATH, "//div[@role='radio' and @aria-label='IOC']")
    #         # ioc.click()
    #
    #         # Step 5: Select LONG TERM
    #         if sl_scenario["longterm"]:
    #             wait.until(
    #                 EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Long Term']"))
    #             ).click()
    #             print("✔ Selected Long Term")
    #         else:
    #             wait.until(
    #                 EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Intraday']"))
    #             ).click()
    #             print("✔ Selected Intraday")
    #         time.sleep(1)
    #
    #         # Step 6: Select DAY or IOC using our new function
    #         select_validity(sl_scenario["validity"])
    #
    #         # Step 7: CLICK BUY
    #         wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Sell']"))
    #         ).click()
    #         print("🟢 BUY button clicked")
    #
    #         time.sleep(3)
    #
    #     print("\n🎉 All 4 scenarios executed successfully!")

    def pending_order_fun(self):

        # plus_btn = self.driver.find_element(By.XPATH, "//figure[@class='absolute top-1/4 right-[10px] cursor-pointer']//*[name()='svg']")
        # for icon in range(2):
        #     self.driver.execute_script("arguments[0].click();", plus_btn)
        self.driver.find_element(*self.qty_input).clear()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.qty_input)
        ).send_keys("7")
        # self.driver.find_element(*self.sign_button).click()
        # self.driver.find_element(*self.password_input).clear()
        # self.driver.find_element(*self.password_input).send_keys(password)

        modify_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class,'owreviewOrderBtn') and normalize-space()='Modify']")
            )
        )
        modify_button.click()
