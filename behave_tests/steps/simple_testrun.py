import requests
from behave import *

@given('we have behave installed')
def step_impl(context):
    pass

@when('we implement a test')
def step_impl(context):
    assert True is not False

@then('behave will test it for us!')
def step_impl(context):
    assert context.failed is False

@then('the main page response will say "{message}"')
def step_impl(context, message):
    base_url = context.test.live_server_url

    request_url = base_url + ''
    resp = requests.get(request_url)

    assert message in resp.text
