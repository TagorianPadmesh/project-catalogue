from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@when('I press the "{button}" button')
def step_press_button(context, button):
    element = context.driver.find_element(
        By.XPATH, f"//button[normalize-space()='{button}']"
    )
    element.click()

@then('I should see "{name}" in the results')
def step_see_text_in_results(context, name):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element((By.ID, "search_results"), name)
    )
    assert found

@then('I should not see "{name}" in the results')
def step_not_see_text_in_results(context, name):
    element = context.driver.find_element(By.ID, "search_results")
    assert name not in element.text

@then('I should see the message "{message}"')
def step_see_message(context, message):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element((By.ID, "flash_message"), message)
    )
    assert found

@when('I visit the "{page_name}"')
def step_visit_page(context, page_name):
    context.driver.get(context.ui_base_url)

@when('I set the "{field}" to "{value}"')
def step_set_field(context, field, value):
    element = context.driver.find_element(By.ID, field.lower())
    element.clear()
    element.send_keys(value)

@when('I change "{field}" to "{value}"')
def step_change_field(context, field, value):
    step_set_field(context, field, value)

@when('I select "{value}" in the "{field}" dropdown')
def step_select_dropdown(context, value, field):
    from selenium.webdriver.support.ui import Select
    element = context.driver.find_element(By.ID, field.lower())
    Select(element).select_by_visible_text(value)

@when('I copy the "{field}" field')
def step_copy_field(context, field):
    context.copied_value = context.driver.find_element(
        By.ID, field.lower()
    ).get_attribute("value")

@when('I paste the "{field}" field')
def step_paste_field(context, field):
    element = context.driver.find_element(By.ID, field.lower())
    element.clear()
    element.send_keys(context.copied_value)

@then('I should see "{value}" in the "{field}" field')
def step_see_field(context, value, field):
    element = context.driver.find_element(By.ID, field.lower())
    assert element.get_attribute("value") == value

@then('I should see "{value}" in the "{field}" dropdown')
def step_see_dropdown(context, value, field):
    from selenium.webdriver.support.ui import Select
    element = context.driver.find_element(By.ID, field.lower())
    assert Select(element).first_selected_option.text == value
