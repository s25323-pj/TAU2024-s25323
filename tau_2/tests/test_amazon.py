from common import browsers, accept_privacy, EC, WebDriverWait, By



def test_amazon_com(browser_name, driver):
    driver.get("https://www.amazon.com/")

    try:
        accept_cookies_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "sp-cc-accept"))
        )
        accept_cookies_btn.click()
    except:
        print("Baner cookies się nie pojawił lub ma inny selektor.")

    # Asercja 1: Sprawdzenie tytułu strony
    assert "Amazon" in driver.title, "Tytuł strony nie zawiera 'Amazon'"

    # Asercja 2: Wyszukiwanie produktu
    search_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "twotabsearchtextbox"))
    )
    search_box.clear()
    search_box.send_keys("mouse")
    search_box.submit()

    # Asercja 3: Sprawdzenie, czy są wyniki
    search_results = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, "//div[@data-component-type='s-search-result']"))
    )
    assert len(search_results) > 0, "Brak wyników wyszukiwania dla 'mouse'"

    # Asercja 4: Kliknięcie w pierwszy wynik
    first_result_link = search_results[0].find_element(
        By.XPATH,
        ".//div[contains(@class,'s-image')]"
    )
    first_result_link.click()

    # Asercja 5: Sprawdzenie, czy otworzyła się strona szczegółowa produktu
    product_title = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "productTitle"))
    )
    assert product_title.is_displayed(), "Karta produktu nie została otwarta"

    # Asercja 6: Sprawdzenie ceny
    try:
        price_element = driver.find_element(By.XPATH, "//span[@class='a-price-whole']")
    except:
        try:
            price_element = driver.find_element(By.XPATH, "//span[contains(@class,'a-price')]")
        except:
            price_element = None

    assert price_element, "Brak elementu z ceną produktu"

    # Asercja 7: Dodanie do koszyka
    add_to_cart_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "add-to-cart-button"))
    )
    add_to_cart_btn.click()

    # Asercja 8: Potwierdzenie dodania
    cart_count = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "nav-cart-count"))
    )
    assert cart_count.text != "0", "Koszyk nie został zaktualizowany"

    # Asercja 9: Przejście do koszyka
    cart_link = driver.find_element(By.ID, "nav-cart")
    cart_link.click()

    # Asercja 10: Sprawdzenie zawartości koszyka
    cart_items = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".sc-list-item"))
    )
    assert len(cart_items) > 0, "Koszyk jest pusty mimo dodania produktu"


def run_amazon_tests():

    for browser_name, browser_driver in browsers.items():
        driver = browser_driver()
        try:
            test_amazon_com(browser_name, driver)
        finally:
            driver.quit()

if __name__ == "__main__":
    run_amazon_tests()