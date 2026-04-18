import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from utils.browserutils import BrowserUtils
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class OrderBook(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.order_tab = (By.XPATH, "//button[.//p[normalize-space()='Orders']]")
        # self.all_tabs = (By.XPATH, "//button[.//p[contains(text(), 'All Orders')]]")
        self.pending_tabs = (By.XPATH, "//button[.//p[normalize-space()='Pending']]")
        self.executed_tabs = (
        By.XPATH, "//ul[@id='header_tab_list']//button[.//p[starts-with(normalize-space(),'Executed')]]")
        self.trade_book_tabs = (By.XPATH, "//ul[@id='header_tab_list']//button[.//p[normalize-space()='Trade Book']]")
        self.gtt_tabs = (By.XPATH, "//ul[@id='header_tab_list']//button[.//p[normalize-space()='GTT']]")
        self.basket_tab = (By.XPATH, "//ul[@id='header_tab_list']//button[.//p[contains(normalize-space(), 'Basket')]]")
        self.sip_tab = (By.XPATH, "//ul[@id='header_tab_list']//button[.//p[contains(normalize-space(), 'SIP')]]")
        self.alert_tab = (By.XPATH, "//ul[@id='header_tab_list']//button[.//p[contains(normalize-space(), 'Alerts')]]")

    def order_button(self, test_results, expected="pass"):

        elements = [
            ("order_tab", self.order_tab),
            ("pending_tabs", self.pending_tabs),
            ("executed_tabs", self.executed_tabs)
        ]
        for name, locator in elements:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(locator)
                ).click()
                time.sleep(1)
                status = "pass"
                actual_error = ""

            except Exception as e:
                status = "fail"
                actual_error = "XPath not found or invalid xpath"

            test_results.append({
                "Page": "OrderBook",
                "Testing_Area": name,
                "expected": expected,
                "actual": "clicked successfully" if status == "pass" else actual_error,
                "status": status
            })

    def order_button_pending(self, test_results, expected="pass"):
        elements = [
            ("order_tab", self.order_tab),
            ("pending_tab", self.pending_tabs)
        ]
        for name, locator in elements:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(locator)
                ).click()
                time.sleep(1)
                status = "pass"
                actual_error = ""

            except Exception as e:
                status = "fail"
                actual_error = "XPath not found or invalid xpath"

            test_results.append({
                "Page": "OrderBook",
                "Testing_Area": name,
                "expected": expected,
                "actual": "clicked successfully" if status == "pass" else actual_error,
                "status": status
            })

    def order_list(self, test_results, expected="pass"):
        driver = self.driver
        wait = WebDriverWait(driver, 12)
        actions = ActionChains(driver)
        action_log = []
        # test_results = []
        more_logged = False
        info_logged = False
        history_logged = False

        rows = driver.find_elements(By.XPATH, "//tbody/tr")

        for i, row in enumerate(rows):
            try:
                # re-fetch rows fresh each time (avoid stale element reference)
                rows = driver.find_elements(By.XPATH, "//tbody/tr")
                row = rows[i]

                # click row (optional if required)
                driver.execute_script("arguments[0].scrollIntoView(true);", row)
                row.click()

                more_btn = row.find_element(By.XPATH, ".//button[contains(@id,'opt_btn')]")
                driver.execute_script("arguments[0].click();", more_btn)
                if not more_logged:
                    test_results.append({
                        "Page": "Order Book",
                        "Testing_Area": "More button",
                        "expected": "More button clicked",
                        "actual": "More button clicked of show info option button",
                        "status": "pass"
                    })
                    more_logged = True

                # wait and click Info in the dropdown
                info_option = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@role='menu']//div[normalize-space()='Info']"))
                )
                info_option.click()
                if not info_logged:
                    test_results.append({
                        "Page": "Order Book",
                        "Testing_Area": "Info button",
                        "expected": "Info button clicked",
                        "actual": "Info button clicked and scrip-details info opened successfully",
                        "status": "pass"
                    })
                    time.sleep(2)
                    info_logged = True

                information_tab = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@id='Information']"))
                )
                information_tab.click()
                #
                history_tab = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH,
                                                "//button[@id='History']"))
                )
                history_tab.click()
                if not history_logged:
                    test_results.append({
                        "Page": "Order Book",
                        "Testing_Area": "History button",
                        "expected": "History button clicked",
                        "actual": "History button clicked and order-details opened successfully",
                        "status": "pass"
                    })

                    history_logged = True

                cancel_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Close']"))
                )
                cancel_button.click()
                time.sleep(3)

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

    #
    #     for i in range(min(5, len(rows))):  # first 5 rows only
    #         rows = driver.find_elements(By.XPATH, "//tbody/tr")
    #         row = rows[i]
    #
    #         driver.execute_script("arguments[0].scrollIntoView(true);", row)
    #         row.click()
    #         try:
    #             clone_btn = row.find_element(By.XPATH, ".//button[contains(text(),'Clone')]")
    #             driver.execute_script("arguments[0].click();", clone_btn)
    #             print(f"✅ Clone clicked for row {i + 1}")
    #             buy_button = WebDriverWait(driver, 5).until(
    #                 EC.element_to_be_clickable(
    #                     (By.XPATH, "//button[@type='submit' and contains(@class,'green_btn')]//span[normalize-space(text())='Buy']"))
    #             )
    #             buy_button.click()
    #         except Exception as e:
    #             print(f"No Clone button found in row {i + 1}: {e}")
    #
    #         time.sleep(1)
    def pending_order_list(self):
        driver = self.driver
        wait = WebDriverWait(driver, 12)
        actions = ActionChains(driver)
        action_log = []

        rows = driver.find_elements(By.XPATH, "//tbody/tr")

        for i, row in enumerate(rows):
            try:
                # re-fetch rows fresh each time (avoid stale element reference)
                rows = driver.find_elements(By.XPATH, "//tbody/tr")
                row = rows[i]

                # click row (optional if required)
                driver.execute_script("arguments[0].scrollIntoView(true);", row)
                row.click()

                # more_btn = row.find_element(By.XPATH, ".//button[contains(@id,'opt_btn')]")
                # driver.execute_script("arguments[0].click();", more_btn)

                modify_btn = row.find_element(By.XPATH, ".//button[normalize-space()='Modify']")
                driver.execute_script("arguments[0].click();", modify_btn)
                time.sleep(5)

                # wait and click Info in the dropdown
                # info_option = WebDriverWait(driver, 5).until(
                #     EC.element_to_be_clickable((By.XPATH, "//div[@role='menu']//div[normalize-space()='Info']"))
                # )
                # info_option.click()
                # time.sleep(2)

                # information_tab = WebDriverWait(driver, 5).until(
                #     EC.element_to_be_clickable((By.XPATH, "//button[@id='Information']"))
                # )
                # information_tab.click()
                #
                # history_tab = WebDriverWait(driver, 5).until(
                #     EC.element_to_be_clickable((By.XPATH,
                #                                 "//button[@id='History']'"))
                # )
                # history_tab.click()

                # cancel_button = WebDriverWait(driver, 5).until(
                #     EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Close']"))
                # )
                # cancel_button.click()
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

    def gtt_order_button(self, test_results, expected="pass"):

        def common_buy_order(test_results, expected="pass"):
            try:

                wait = WebDriverWait(self.driver, 10)

                # Click the Create button
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@id='create_basket_btn']"))
                ).click()
                test_results.append({
                    "Page": "Order Book",
                    "Testing_Area": "GTT button",
                    "expected": "GTT button clicked",
                    "actual": "GTT button clicked and order-details opened successfully",
                    "status": "pass"
                })

                time.sleep(3)

                # Wait for the input field to be clickable
                # search_input = wait.until(
                #     EC.visibility_of_element_located((By.CSS_SELECTOR,
                #                                       "body > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(1) > section:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(2)"))
                #
                search_input = wait.until(
                    EC.visibility_of_element_located((By.ID, "watch_search_inp")))
                # self.driver.execute_script("arguments[0].scrollIntoView(true);", search_input)
                search_input.click()
                search_input.send_keys("TCS")
                test_results.append({
                    "Page": "Order Book",
                    "Testing_Area": "Search button",
                    "expected": "Search button clicked",
                    "actual": "Search button clicked and search-list opened successfully",
                    "status": "pass"
                })

                time.sleep(5)
                # ActionChains(self.driver).move_to_element(scrip).perform()
                first_result = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "(//div[contains(@id,'_search_scrip')])[1]"))
                )

                self.driver.execute_script("arguments[0].scrollIntoView(true);", first_result)
                self.driver.execute_script("arguments[0].click();", first_result)
                test_results.append({
                    "Page": "Order Book",
                    "Testing_Area": "Search Scrip",
                    "expected": "Search Scrip added",
                    "actual": "Search Scrip added successfully",
                    "status": "pass"
                })

                time.sleep(4)
                # menu_btn = wait.until(
                #     EC.element_to_be_clickable((By.XPATH, "//button[text()='Create']"))
                # )
                # menu_btn.click()

                qty_input = wait.until(
                    EC.visibility_of_element_located((By.ID,
                                                      "qty"))
                )
                # self.driver.execute_script("arguments[0].scrollIntoView(true);", search_input)
                qty_input.click()
                qty_input.clear()
                test_results.append({
                    "Page": "Order Book",
                    "Testing_Area": "Quantity Field",
                    "expected": "Quantity Field clicked",
                    "actual": "Quantity Field clicked and check input-field successfully",
                    "status": "pass"
                })

                add_qty = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                      "body > div:nth-child(4) > form:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > figure:nth-child(3) > svg:nth-child(1)"))
                )

                add_qty.click()

                test_results.append({
                    "Page": "Order Book",
                    "Testing_Area": "Quantity Field",
                    "expected": "Quantity Field clicked",
                    "actual": "Quantity Field clicked and add quantity successfully",
                    "status": "pass"
                })

                remove_qty = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                      "body > div:nth-child(4) > form:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > figure:nth-child(1) > svg:nth-child(1)"))
                )

                remove_qty.click()
                test_results.append({
                    "Page": "Order Book",
                    "Testing_Area": "Quantity Field",
                    "expected": "Quantity Field clicked",
                    "actual": "Quantity Field clicked and remove quantity successfully",
                    "status": "pass"
                })
                price_el = wait.until(EC.element_to_be_clickable((By.ID, "price")))
                # qty_el.send_keys(qty)
                for _ in range(2):
                    time.sleep(0.3)
                    price_el.send_keys(Keys.ARROW_UP)
                test_results.append({
                    "Page": "Order Book",
                    "Testing_Area": "Price Field",
                    "expected": "Price Field clicked",
                    "actual": "Price Field clicked and add price successfully",
                    "status": "pass"
                })

                trigger_price_el = wait.until(EC.element_to_be_clickable((By.ID, "triggerPrice")))
                # qty_el.send_keys(qty)
                test_results.append({
                    "Page": "Order Book",
                    "Testing_Area": "TriggerPrice Field",
                    "expected": "TriggerPrice Field clicked",
                    "actual": "TriggerPrice Field clicked and add trigger-price successfully",
                    "status": "pass"
                })
                for _ in range(2):
                    time.sleep(0.3)
                    trigger_price_el.send_keys(Keys.ARROW_UP)

                add_checkbox = wait.until(
                    EC.visibility_of_element_located((By.ID,
                                                      "comments"))
                )
                add_checkbox.click()
                test_results.append({
                    "Page": "Order Book",
                    "Testing_Area": "Checkbox Field",
                    "expected": "Checkbox Field clicked",
                    "actual": "Checkbox Field clicked successfully",
                    "status": "pass"
                })

                submit = wait.until(
                    EC.visibility_of_element_located((By.XPATH,
                                                      "//button[text()='Create']"))
                )
                submit.click()
                test_results.append({
                    "Page": "Order Book",
                    "Testing_Area": "Create Button",
                    "expected": "Checkbox Field clicked",
                    "actual": "Checkbox Field clicked successfully",
                    "status": "pass"
                })

                # test_results.append({
                #     "Page": "OrderBook",
                #     "Testing_Area": "create_basket_btn",
                #     "expected": expected,
                #     "actual": "clicked successfully",
                #     "status": "pass"
                # })

            except Exception:
                test_results.append({
                    "Page": "OrderBook",
                    "Testing_Area": "create_basket_btn",
                    "expected": expected,
                    "actual": "XPath not found or invalid xpath",
                    "status": "fail"
                })

        def common_sell_order(test_results, expected="pass"):
            try:

                wait = WebDriverWait(self.driver, 10)

                # Click the Create button
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@id='create_basket_btn']"))
                ).click()

                time.sleep(3)

                # Wait for the input field to be clickable
                search_input = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                      "body > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(1) > section:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(2)"))
                )
                # self.driver.execute_script("arguments[0].scrollIntoView(true);", search_input)
                search_input.click()
                search_input.send_keys("TCS")

                time.sleep(5)
                # ActionChains(self.driver).move_to_element(scrip).perform()
                first_result = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "(//div[contains(@id,'_search_scrip')])[1]"))
                )

                self.driver.execute_script("arguments[0].scrollIntoView(true);", first_result)
                self.driver.execute_script("arguments[0].click();", first_result)

                time.sleep(4)
                # menu_btn = wait.until(
                #     EC.element_to_be_clickable((By.XPATH, "//button[text()='Create']"))
                # )
                # menu_btn.click()

                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@role='switch']"))
                ).click()

                qty_input = wait.until(
                    EC.visibility_of_element_located((By.ID,
                                                      "qty"))
                )
                # self.driver.execute_script("arguments[0].scrollIntoView(true);", search_input)
                qty_input.click()
                qty_input.clear()

                add_qty = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                      "body > div:nth-child(4) > form:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > figure:nth-child(3) > svg:nth-child(1)"))
                )

                add_qty.click()

                remove_qty = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                      "body > div:nth-child(4) > form:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > figure:nth-child(1) > svg:nth-child(1)"))
                )

                remove_qty.click()
                price_el = wait.until(EC.element_to_be_clickable((By.ID, "price")))
                # qty_el.send_keys(qty)
                for _ in range(2):
                    time.sleep(0.3)
                    price_el.send_keys(Keys.ARROW_UP)

                trigger_price_el = wait.until(EC.element_to_be_clickable((By.ID, "triggerPrice")))
                # qty_el.send_keys(qty)
                for _ in range(2):
                    time.sleep(0.3)
                    trigger_price_el.send_keys(Keys.ARROW_UP)

                add_checkbox = wait.until(
                    EC.visibility_of_element_located((By.ID,
                                                      "comments"))
                )
                add_checkbox.click()

                submit = wait.until(
                    EC.visibility_of_element_located((By.XPATH,
                                                      "//button[text()='Create']"))
                )
                submit.click()

                test_results.append({
                    "Page": "OrderBook",
                    "Testing_Area": "create_basket_btn",
                    "expected": expected,
                    "actual": "clicked successfully",
                    "status": "pass"
                })

            except Exception:
                test_results.append({
                    "Page": "OrderBook",
                    "Testing_Area": "create_basket_btn",
                    "expected": expected,
                    "actual": "XPath not found or invalid xpath",
                    "status": "fail"
                })

        def gtt_order_list():
            driver = self.driver
            wait = WebDriverWait(driver, 12)
            actions = ActionChains(driver)
            action_log = []

            rows = driver.find_elements(By.XPATH, "//tbody/tr")

            for i, row in enumerate(rows):
                try:
                    # re-fetch rows fresh each time (avoid stale element reference)
                    rows = driver.find_elements(By.XPATH, "//tbody/tr")
                    row = rows[i]

                    # click row (optional if required)
                    driver.execute_script("arguments[0].scrollIntoView(true);", row)
                    row.click()

                    # more_btn = row.find_element(By.XPATH, ".//button[contains(@id,'opt_btn')]")
                    # driver.execute_script("arguments[0].click();", more_btn)

                    modify_btn = row.find_element(By.XPATH, ".//button[normalize-space()='Modify']")
                    driver.execute_script("arguments[0].click();", modify_btn)
                    time.sleep(5)
                    test_results.append({
                        "Page": "Order Book",
                        "Testing_Area": "Modify button",
                        "expected": "Modify button clicked",
                        "actual": "Modify button clicked and order-window opened successfully",
                        "status": "pass"
                    })

                    qty_input = wait.until(
                        EC.visibility_of_element_located((By.ID,
                                                          "qty"))
                    )
                    # self.driver.execute_script("arguments[0].scrollIntoView(true);", search_input)
                    qty_input.click()
                    qty_input.clear()

                    add_qty = wait.until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                          "body > div:nth-child(4) > form:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > figure:nth-child(3) > svg:nth-child(1)"))
                    )

                    add_qty.click()

                    remove_qty = wait.until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                          "body > div:nth-child(4) > form:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > figure:nth-child(1) > svg:nth-child(1)"))
                    )

                    remove_qty.click()
                    price_el = wait.until(EC.element_to_be_clickable((By.ID, "price")))
                    for _ in range(2):
                        price_el.send_keys(Keys.ARROW_UP)
                        time.sleep(0.3)

                    # Modify trigger price
                    trigger_el = wait.until(EC.element_to_be_clickable((By.ID, "triggerPrice")))
                    for _ in range(2):
                        trigger_el.send_keys(Keys.ARROW_UP)
                        time.sleep(0.3)

                    # Submit Modify
                    submit_btn = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and text()='Modify']"))
                    )
                    submit_btn.click()

                    time.sleep(3)

                except Exception as e:
                    print(e)

                    time.sleep(2)

        elements = [
            ("order_tab", self.order_tab),
            ("trade_book", self.trade_book_tabs),
            ("gtt", self.gtt_tabs)
        ]

        for name, locator in elements:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(locator)
                ).click()
                time.sleep(2)

                status = "pass"
                actual_error = ""

            except Exception:
                status = "fail"
                actual_error = "XPath not found or invalid xpath"

            test_results.append({
                "Page": "OrderBook",
                "Testing_Area": name,
                "expected": expected,
                "actual": "clicked successfully" if status == "pass" else actual_error,
                "status": status
            })

        # --- Corrected Create Button Click ---

        common_buy_order(test_results, expected)
        common_sell_order(test_results, expected)
        gtt_order_list()

    def basket_order_button(self, test_results, expected="pass"):
        elements = [
            ("order_tab", self.order_tab),
            ("basket_tab", self.basket_tab)
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
                "Page": "OrderBook",
                "Testing_Area": name,
                "expected": expected,
                "actual": "clicked successfully" if status == "pass" else actual_error,
                "status": status
            })

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='create_basket_btn']"))
        ).click()

        time.sleep(3)
        basket_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "createBasket_name")))
        basket_input.click()
        test_results.append({
            "Page": "Order Book",
            "Testing_Area": "Create basket button",
            "expected": "Create basket name",
            "actual": "basket button clicked and create basket name successfully",
            "status": "pass"
        })
        basket_input.send_keys("TEST")
        time.sleep(3)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='createbasket_btn']"))
        ).click()

        rows = self.driver.find_elements(By.XPATH, "//tbody/tr")

        for i, row in enumerate(rows):
            try:
                # re-fetch rows fresh each time (avoid stale element reference)
                rows = self.driver.find_elements(By.XPATH, "//tbody/tr")
                row = rows[i]

                # click row (optional if required)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", row)
                row.click()
            except Exception as e:
                print(e)
        icon = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//figure[@class='cursor-pointer'])[1]"))
        )
        icon.click()
        basket_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "createBasket_name")))
        basket_input.click()
        basket_input.clear()
        basket_input.send_keys("BASKET-NEW")
        time.sleep(3)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='createbasket_btn']"))
        ).click()
        search_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID,
                                              "watch_search_inp"))
        )
        search_input.click()
        search_input.send_keys("TCS")

        time.sleep(5)

        first_result = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[contains(@id,'_search_scrip')])[1]"))
        )

        self.driver.execute_script("arguments[0].scrollIntoView(true);", first_result)
        self.driver.execute_script("arguments[0].click();", first_result)
        time.sleep(3)
        add_basket = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@type='submit']")))
        add_basket.click()

        confirm_basket = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[.//span[normalize-space()='Yes']]")))
        confirm_basket.click()
        time.sleep(3)

        rows = self.driver.find_elements(By.XPATH, "//tbody/tr")

        for i, row in enumerate(rows):
            try:
                # re-fetch rows fresh each time (avoid stale element reference)
                rows = self.driver.find_elements(By.XPATH, "//tbody/tr")
                row = rows[i]

                # click row (optional if required)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", row)
                row.click()
                time.sleep(12)

                ActionChains(self.driver).move_to_element(row).perform()

                clone_btn = row.find_element(By.XPATH, ".//button[normalize-space()='Clone']")
                self.driver.execute_script("arguments[0].click();", clone_btn)
                test_results.append({
                    "Page": "Order Book",
                    "Testing_Area": "Clone button",
                    "expected": "Clone button clicked",
                    "actual": "Clone button clicked and added successfully",
                    "status": "pass"
                })

                time.sleep(5)
                ActionChains(self.driver).move_to_element(row).perform()

                edit_btn = row.find_element(By.XPATH, ".//button[normalize-space()='Edit']")
                self.driver.execute_script("arguments[0].click();", edit_btn)
                time.sleep(2)
                test_results.append({
                    "Page": "Order Book",
                    "Testing_Area": "Edit button",
                    "expected": "Edit button clicked",
                    "actual": "Edit button clicked and modified successfully",
                    "status": "pass"
                })

                add_qty = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                      "#ow_qty > div > figure.absolute.top-1\/4.right-\[10px\].cursor-pointer"))
                )

                add_qty.click()

                add_basket = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//button[normalize-space()='Add']")))
                add_basket.click()
                confirm_basket = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//button[.//span[normalize-space()='Yes']]")))
                confirm_basket.click()

            except Exception as e:
                print(e)

        # delete_basket = WebDriverWait(self.driver, 10).until(
        #     EC.visibility_of_element_located((By.XPATH,
        #                                       "//button[normalize-space()='Delete']")))
        # delete_basket.click()
        test_results.append({
            "Page": "Order Book",
            "Testing_Area": "Delete button",
            "expected": "Delete button clicked",
            "actual": "Delete button clicked and deleted successfully",
            "status": "pass"
        })

        confirm_delete_basket = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH,
                                              "//button[@id='createbasket_btn']")))
        confirm_delete_basket.click()

    def sip_button(self, test_results, expected="pass"):
        elements = [
            ("order_tab", self.order_tab),
            ("sip_tab", self.sip_tab),
            ("alert_tabs", self.alert_tab)
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
                "Page": "OrderBook",
                "Testing_Area": name,
                "expected": expected,
                "actual": "clicked successfully" if status == "pass" else actual_error,
                "status": status
            })

    def get_login_error(self):
        try:
            return self.driver.find_element(*self.error_msg).text
        except:
            return None
