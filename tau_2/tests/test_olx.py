from common import browsers, accept_privacy, EC, WebDriverWait, By

def test_olx(browser_name, driver):
    url = "https://www.olx.pl/"
    driver.get(url)
    accept_privacy(driver, [(By.ID, "onetrust-accept-btn-handler")])

    # Asercja 1: Sprawdź tytuł
    assert "OLX" in driver.title, f"{browser_name}: Tytuł strony nie zawiera 'OLX'"

    # Asercja 2: Sprawdź widoczność pola wyszukiwania
    search_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "search"))
    )
    assert search_input.is_displayed(), f"{browser_name}: Pole wyszukiwania nie jest widoczne"

    # Asercja 3: Wpisz tekst i wyszukaj
    search_input.send_keys("rower")
    search_button = driver.find_element(By.XPATH, "//button[@data-testid='search-submit']")
    assert search_button.is_displayed(), f"{browser_name}: Przycisk szukaj nie jest widoczny"
    search_button.click()

    # Asercja 4: Sprawdź, czy wyniki się wyświetlają
    results_header = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h4[contains(text(),'rower')]"))
    )
    assert results_header.is_displayed(), f"{browser_name}: Brak ogłoszenia z tytułem zawierającym 'rower'"

    # Asercja 5: Przejście na drugą stronę wyników
    second_page_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-testid='pagination-link-2']"))
    )
    second_page_link.click()

    second_page_header = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h4[contains(text(),'rower')]"))
    )
    assert second_page_header.is_displayed(), f"{browser_name}: Druga strona wyników nie jest widoczna"

    # Asercja 6: Wróć do strony głównej
    logo_link = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//a[@href='/']"))
    )
    assert logo_link.is_displayed(), f"{browser_name}: Logo OLX nie jest widoczne"
    logo_link.click()

    # Asercja 7: Sprawdź czy ponownie widzimy pole wyszukiwania
    search_input_home = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "search"))
    )
    assert search_input_home.is_displayed(), f"{browser_name}: Pole wyszukiwania nie jest widoczne po powrocie"

    # Asercja 8: Sprawdź tytuł strony głównej
    assert "OLX" in driver.title, f"{browser_name}: Tytuł strony po powrocie nie zawiera 'OLX'"

def run_olx_tests():
    for browser_name, browser_driver in browsers.items():
        driver = browser_driver()
        try:
            test_olx(browser_name, driver)
        finally:
            driver.quit()

if __name__ == "__main__":
    run_olx_tests()
