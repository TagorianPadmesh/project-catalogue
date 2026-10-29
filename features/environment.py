import os

def before_all(context):
    context.base_url = os.getenv("API_BASE_URL", "http://127.0.0.1:5000")
    context.ui_base_url = os.getenv("UI_BASE_URL", "http://127.0.0.1:3000")
    context.wait_seconds = 5
    # Configure context.driver for your actual Selenium browser setup.

def after_all(context):
    driver = getattr(context, "driver", None)
    if driver:
        driver.quit()
