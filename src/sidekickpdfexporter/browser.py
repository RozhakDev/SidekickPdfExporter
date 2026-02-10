import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

try:
    from subprocess import CREATE_NEW_PROCESS_GROUP
except ImportError:
    CREATE_NEW_PROCESS_GROUP = 0


def setup_driver(headless: bool = True):
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    options.add_argument("--log-level=3") 
    options.page_load_strategy = 'eager'

    try:
        service = ChromeService(ChromeDriverManager().install())

        if os.name == 'nt':
            service.creationflags = CREATE_NEW_PROCESS_GROUP

        driver = webdriver.Chrome(service=service, options=options)
        driver.set_script_timeout(60)
        return driver
    except Exception as e:
        raise RuntimeError(f"Gagal memulai WebDriver: {e}")