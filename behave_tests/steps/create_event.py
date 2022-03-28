from behave import *
import requests

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

use_step_matcher("re")


@given("that I am a registered host of privilege walk events and want to create a event")
def step_impl(context):
    context.username = "12thMan"
    context.password = "SomePassword123"
    context.first_name = "12th"
    context.last_name = "Man"
    context.email = "twelve@testtamu.edu"

    usr = User.objects.create_user(
        context.username,
        context.email,
        context.password
    )
    usr.first_name = context.first_name
    usr.last_name = context.last_name
    usr.save()

    registered_user = User.objects.filter(username="12thMan")

    assert len(registered_user) == 1

    user_auth_token, _ = Token.objects.get_or_create(user=usr)
    context.key = user_auth_token.key



@when("I make an API call to create event API with my correct username")
def step_impl(context):
    data = {
        "name": "New year event"
    }
    headers = {
        'Authorization':'Token '+ context.key
    }

    resp = requests.post(context.test.live_server_url + "/host/events/create/", data, headers=headers)
    assert resp.status_code >= 200 and resp.status_code < 300

    context.api_response_data = resp.json()


@then("I expect the response that gives the status and id of the created event")
def step_impl(context):
    assert context.api_response_data["status"] == "created"
    assert context.api_response_data["id"] != ""


@given("that I am not a registered host of privilege walk and wants to create a event")
def step_impl(context):
    context.username = "11thMan"


@when("I make an API call to create event API with my unregistered username")
def step_impl(context):
    data = {
        "name": "New year event"
    }

    headers = {
        'Authorization':'Token '+ 'xyz'
    }

    resp = requests.post(context.test.live_server_url + "/host/events/create/", data, headers=headers)
    assert resp.status_code >= 400 and resp.status_code < 500

    context.api_response_data = resp.json()


@then("I expect the response that says event cannot be created and user has to be registered")
def step_impl(context):
    assert context.api_response_data["detail"] == "Invalid token."


@given("that I am a registered host of privilege walk events and want to create a event but forgets to give username")
def step_impl(context):
    context.username = "11thMan"


@when("I make an API call to create event API with missing username in request")
def step_impl(context):
    data = {
        "name": "New year event"
    }

    resp = requests.post(context.test.live_server_url + "/host/events/create/", data)
    assert resp.status_code >= 400 and resp.status_code < 500

    context.api_response_data = resp.json()


@then("I expect the response that says event cannot be created and username is required in request")
def step_impl(context):
    assert context.api_response_data["detail"] == "Authentication credentials were not provided."

