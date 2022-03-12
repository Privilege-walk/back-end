from behave import *
import requests

from django.contrib.auth.models import User

use_step_matcher("re")


@given("that I am a registered host of privilege walk events")
def step_impl(context):
    context.username = "12thMan"
    context.password = "SomePassword123"

    usr = User.objects.create_user(
        context.username,
        "twelve@testtamu.edu",
        context.password
    )
    usr.first_name = "12th"
    usr.last_name = "Man"
    usr.save()

    registered_user = User.objects.filter(username="12thMan")

    assert len(registered_user) == 1


@when("I make an API call to the login API with my correct username and password")
def step_impl(context):
    data = {
        "username": context.username,
        "password": context.password,
    }

    resp = requests.post(context.test.live_server_url + "/auth/login/", data)
    assert resp.status_code >= 200 and resp.status_code < 300

    context.api_response_data = resp.json()


@then("I expect the response to tell me that I have logged in successfully")
def step_impl(context):
    assert context.api_response_data["status"] == True


@step("Also give me a token that I can use in the future to authenticate to the back-end")
def step_impl(context):
    assert "token" in context.api_response_data