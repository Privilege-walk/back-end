from behave import *
import requests

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

use_step_matcher("re")


@given("that I am a registered host of privilege walk events and exists events on my username")
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

    data = {
        "name": "New year event"
    }
    headers = {
        'Authorization':'Token '+ context.key
    }

    resp = requests.post(context.test.live_server_url + "/host/events/create/", data, headers=headers)


@when("I make an API call to the get events API with my correct username")
def step_impl(context):
    headers = {
        'Authorization':'Token '+ context.key
    }

    resp = requests.get(context.test.live_server_url + "/host/events/all/", headers=headers)
    assert resp.status_code >= 200 and resp.status_code < 300

    context.api_response_data = resp.json()


@then("I expect the response that gives the list of events on my username as host")
def step_impl(context):
    assert context.api_response_data["events"][0]["name"] == "New year event"



@given("that I am a registered host of privilege walk events and there exists no events on my username")
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


@when("I make an API call to the get events API with my username")
def step_impl(context):
    headers = {
        'Authorization':'Token '+ context.key
    }

    resp = requests.get(context.test.live_server_url + "/host/events/all/", headers=headers)
    assert resp.status_code >= 200 and resp.status_code < 300

    context.api_response_data = resp.json()


@then("I expect the response that gives the empty list as response")
def step_impl(context):
    assert context.api_response_data["events"] == []


@given("that I am a registered host of privilege walk events and forgot my username")
def step_impl(context):
    pass


@when("I make an API call to the get events API with wrong username")
def step_impl(context):
    resp = requests.get(context.test.live_server_url + "/host/events/all/")
    assert resp.status_code >= 400 and resp.status_code < 500

    context.api_response_data = resp.json()


@then("I expect the response that says username doesn't exists")
def step_impl(context):
    assert context.api_response_data["detail"] == "Authentication credentials were not provided."