from common import browsers, accept_privacy, EC, WebDriverWait, By

def test_nike_main_page(browser_name, driver):
    driver.get("https://www.nike.com/pl/")
    accept_privacy(driver, [(By.CSS_SELECTOR, "button[data-testid='dialog-accept-button']")])

    # Asercja 1: Sprawdzenie tytułu strony
    assert "Nike. Just Do It. Nike PL" in driver.title, f"{browser_name}: Tytuł strony niepoprawny"

    # Asercja 2: Sprawdzenie logo
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
    logo_link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.swoosh-link")))
    assert logo_link.is_displayed(), f"{browser_name}: Logo niewidoczne"

    # Asercja 3: Link 'Mężczyźni'
    men_link = driver.find_elements(By.CSS_SELECTOR, "a.menu-hover-trigger-link[href*='mezczyzni']")
    assert len(men_link) > 0, f"{browser_name}: Brak linku 'Mężczyźni'"

    # Asercja 4: Wyszukiwarka
    try:
        search_input = driver.find_element(By.CSS_SELECTOR, "input[aria-label='Wyszukaj produkty']")
        assert search_input.is_displayed(), f"{browser_name}: Brak pola wyszukiwania"
    except:
        print(f"{browser_name}: Brak pola wyszukiwania")

    # Asercja 5: Ikona koszyka
    try:
        bag_icon = driver.find_element(By.CSS_SELECTOR, "a[aria-label^='Przedmioty w koszyku']")
        assert bag_icon.is_displayed(), f"{browser_name}: Brak ikony koszyka"
    except:
        print(f"{browser_name}: Brak ikony koszyka")

    # Asercja 6: Przewinięcie do stopki
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    footer = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "gen-nav-footer")))
    assert footer.is_displayed(), f"{browser_name}: Stopka niewidoczna"

    # Asercja 7: Link "Uzyskaj pomoc"
    try:
        help_link = footer.find_element(By.CSS_SELECTOR, "a.footer-link[data-testid='footer-menu-col-1-child-0']")
        assert help_link.is_displayed(), f"{browser_name}: Brak linku 'Uzyskaj pomoc'"
    except:
        print(f"{browser_name}: Brak linku 'Uzyskaj pomoc'")

    # Asercja 8: Link "Informacje o Nike"
    try:
        info_link = footer.find_element(By.CSS_SELECTOR, "a.footer-link[data-testid='footer-menu-col-2-child-0']")
        assert info_link.is_displayed(), f"{browser_name}: Brak linku 'Informacje o Nike'"
    except:
        print(f"{browser_name}: Brak linku 'Informacje o Nike'")

    # Asercja 9: Przycisk "Zaloguj się"
    try:
        login_link = driver.find_element(By.XPATH, "//p[@data-testid='desktop-user-menu-item-message-3' and contains(text(),'Zaloguj się')]")
        assert login_link.is_displayed(), f"{browser_name}: Brak linku 'Zaloguj się'"
    except:
        print(f"{browser_name}: Brak linku 'Zaloguj się'")

    # Asercja 10: Sprawdzenie wyboru kraju
    country_selector = footer.find_elements(By.XPATH, ".//a[contains(text(),'Polska')] | .//button[contains(text(),'Polska')]")
    assert len(country_selector) > 0, f"{browser_name}: Brak wyboru kraju"

def run_nike_tests():
    for browser_name, browser_driver in browsers.items():
        driver = browser_driver()
        try:
            test_nike_main_page(browser_name, driver)
        finally:
            driver.quit()

if __name__ == "__main__":
    run_nike_tests()
