from common import browsers, accept_privacy, EC, WebDriverWait, By
from time import sleep

def test_otomoto(browser_name, driver):
    url = "https://www.otomoto.pl/"
    driver.get(url)

    # Akceptacja polityki prywatności
    accept_privacy(driver, [(By.ID, "onetrust-accept-btn-handler")])

    # Asercja 1: Sprawdź tytuł strony
    assert "OTOMOTO" in driver.title.upper(), f"{browser_name}: Tytuł strony nie zawiera 'Otomoto'"

    # Asercja 2: Zlokalizuj formularz wyszukiwania
    search_form = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//article[@aria-label='Czego szukasz?']//form[@method='post']"))
    )
    assert search_form.is_displayed(), f"{browser_name}: Formularz wyszukiwania nie jest widoczny"

    # Asercja 3: Wybór marki pojazdu
    brand_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@aria-label='Marka pojazdu']//input[@type='text' and not(@disabled)]"))
    )
    assert brand_input.is_displayed(), f"{browser_name}: Pole wyboru marki nie jest widoczne lub aktywne"
    brand_input.clear()
    brand_input.send_keys("BMW")

    bmw_option = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@role='radio' and contains(@aria-label,'BMW')]"))
    )
    assert bmw_option.is_displayed(), f"{browser_name}: Opcja BMW nie jest widoczna w dropdownie"
    bmw_option.click()

    # Asercja 4: Wybór modelu pojazdu
    model_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@aria-label='Model pojazdu']//input[@type='text']"))
    )

    WebDriverWait(driver, 10).until(
        lambda d: d.find_element(By.XPATH, "//div[@aria-label='Model pojazdu']//input[@type='text']").get_attribute("disabled") is None
    )
    assert model_input.is_displayed(), f"{browser_name}: Pole wyboru modelu nie jest widoczne lub nadal wyłączone"

    model_input.click()
    model_input.clear()
    model_input.send_keys("Seria 3")

    seria_3_checkbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@role='checkbox' and contains(.,'Seria 3')]"))
    )

    driver.execute_script("arguments[0].click();", seria_3_checkbox)

    WebDriverWait(driver, 10).until(
        lambda d: d.find_element(By.XPATH, "//div[@role='checkbox' and contains(.,'Seria 3')]").get_attribute(
            "aria-checked") == "true"
    )
    from selenium.webdriver.common.keys import Keys
    model_input.send_keys(Keys.ESCAPE)
    sleep(1)

    # Asercja 5: Kliknij przycisk "Pokaż ogłoszenia"
    show_offers_button = WebDriverWait(search_form, 10).until(
        EC.element_to_be_clickable((By.XPATH, ".//button[@type='submit']"))
    )
    assert show_offers_button.is_displayed(), f"{browser_name}: Przycisk 'Szukaj' nie jest widoczny"
    show_offers_button.click()

    # Asercja 6: Sprawdź wyniki wyszukiwania
    results_header = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(),'BMW')]"))
    )
    assert results_header.is_displayed(), f"{browser_name}: Brak wyników wyszukiwania dla BMW"

    # Asercja 7: Sprawdź, czy pojawiły się ogłoszenia
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-testid='search-results'] article[data-id]"))
    )

    ads = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='search-results'] article[data-id]")
    assert len(ads) > 0, f"{browser_name}: Brak ogłoszeń w wynikach wyszukiwania"

    # Asercja 8: Sprawdź obecność filtra 'BMW'
    filter_bmw_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//input[@aria-label='Marka pojazdu' and contains(@placeholder,'BMW')]")
        )
    )

    assert filter_bmw_input.is_displayed(), f"{browser_name}: Filtr marki 'BMW' nie jest widoczny"

    # Asercja 9: Powrót na stronę główną
    home_logo_img = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//img[@alt='Logo']"))
    )
    assert home_logo_img.is_displayed(), f"{browser_name}: Logo nie jest widoczne"

    home_link = home_logo_img.find_element(By.XPATH, "./ancestor::a")
    assert home_link.is_displayed(), f"{browser_name}: Link do strony głównej (logo) nie jest widoczny"

    home_link.click()

    home_search_form = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//article[@aria-label='Czego szukasz?']//form[@method='post']"))
    )
    assert home_search_form.is_displayed(), f"{browser_name}: Formularz wyszukiwania nie jest widoczny po powrocie"


def run_otomoto_tests():
    for browser_name, browser_driver in browsers.items():
        driver = browser_driver()
        try:
            test_otomoto(browser_name, driver)
        finally:
            driver.quit()

if __name__ == "__main__":
    run_otomoto_tests()
