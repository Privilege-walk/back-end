from behave import *
import requests

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

use_step_matcher("re")


@given("that I am a unregistered participant of a event")
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
    context.event_api_response_data = resp.json()
    context.eventId = context.event_api_response_data["id"]


@when("I make an API call to the participant registration API with event id")
def step_impl(context):
    data = {
        "event_id": context.eventId
    }
    headers = {
        'Authorization':'Token '+ context.key
    }

    resp = requests.post(context.test.live_server_url + "/walk/register_participant/", data, headers=headers)
    assert resp.status_code >= 200 and resp.status_code < 300

    context.api_response_data = resp.json()


@then("I expect the response to tell me the re is successful and give a participant code")
def step_impl(context):
    assert context.api_response_data["status"] == "registered"



@given("that I am a participant and wants to join an event and forgets to give event id")
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


@when("I make an API call to the participant registration API without giving event id")
def step_impl(context):
    data = {
        "event_id": ''
    }
    headers = {
        'Authorization':'Token '+ context.key
    }

    resp = requests.post(context.test.live_server_url + "/walk/register_participant/", data, headers=headers)
    assert resp.status_code >= 400 and resp.status_code < 500

    context.api_response_data = resp.json()


@then("I expect the response to tell me that the registration is not successful")
def step_impl(context):
    assert context.api_response_data["message"] == "Event not found, try a different event ID"

@given("that I am a participant and want to join an event by giving wrong event id")
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


@when("I make an API call to the participant registration API with wrong event id")
def step_impl(context):
    data = {
        "event_id": '12345'
    }
    headers = {
        'Authorization':'Token '+ context.key
    }

    resp = requests.post(context.test.live_server_url + "/walk/register_participant/", data, headers=headers)
    assert resp.status_code >= 400 and resp.status_code < 500

    context.api_response_data = resp.json()


@then("I expect the response to tell me that the registration is not successful and event id is wrong")
def step_impl(context):
    assert context.api_response_data["message"] == "Event not found, try a different event ID"