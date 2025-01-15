from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browsers = {
    "Chrome": webdriver.Chrome,
    "Edge": webdriver.Edge,
    "Firefox": webdriver.Firefox
}

def accept_privacy(driver, accept_button_selectors):
    for selector in accept_button_selectors:
        try:
            btn = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(selector)
            )
            btn.click()
            break
        except:
            pass
