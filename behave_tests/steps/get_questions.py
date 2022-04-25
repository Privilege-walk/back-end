from behave import *
import requests

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

use_step_matcher("re")


@given("that I am a registered host of privilege walk events and want to get questions and answer choices for the event")
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
        "name": "New year event",
        "x_label_min": "Some text to be displayed on the graph",
        "x_label_max": "Something else you want to be displayed on the graph",
    }
    headers = {
        'Authorization':'Token '+ context.key
    }

    resp = requests.post(context.test.live_server_url + "/host/events/create/", data, headers=headers)
    context.event_api_response_data = resp.json()
    context.eventId = context.event_api_response_data["id"]
    data = {
        "event_id": context.eventId,
        "title": "The question's title goes here",
        "choices": [
            {
                "description": "Pizza",
                "value": 1
            },
            {
                "description": "Ice Cream",
                "value": 2
            },
            {
                "description": "Salt Water",
                "value": -1
            }
        ]
    }
    headers = {
        'Authorization':'Token '+ context.key
    }

    resp = requests.post(context.test.live_server_url + "/host/qa/create/", data, headers=headers)



@when("I make an API call to get questions API with my correct username and correct eventid")
def step_impl(context):
    headers = {
        'Authorization':'Token '+ context.key
    }

    resp = requests.get(context.test.live_server_url + "/host/qa/eventwise_qas/?event_id="+str(context.eventId), headers=headers)
    assert resp.status_code >= 200 and resp.status_code < 300

    context.api_response_data = resp.json()


@then("I expect the response that gives the list of questions and answer choices related to that event")
def step_impl(context):
    assert context.api_response_data["id"] == context.eventId
    assert context.api_response_data["questions"][0]["description"] == "The question's title goes here"


@given("that I am a registered host of privilege walk and wants to get questions for the event that has no questions added to it")
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
        "name": "New year event",
        "x_label_min": "Some text to be displayed on the graph",
        "x_label_max": "Something else you want to be displayed on the graph",
    }
    headers = {
        'Authorization':'Token '+ context.key
    }

    resp = requests.post(context.test.live_server_url + "/host/events/create/", data, headers=headers)
    context.event_api_response_data = resp.json()
    context.eventId = context.event_api_response_data["id"]


@when("I make an API call to get questions API with my username and event id")
def step_impl(context):
    headers = {
        'Authorization':'Token '+ context.key
    }

    resp = requests.get(context.test.live_server_url + "/host/qa/eventwise_qas/?event_id="+str(context.eventId), headers=headers)
    assert resp.status_code >= 200 and resp.status_code < 300

    context.api_response_data = resp.json()


@then("I expect the empty list of questions in response")
def step_impl(context):
    assert context.api_response_data["id"] == context.eventId


@given("that I am a registered host of privilege walk and wants to get questions by giving wrong event id")
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



@when("I make an API call to get questions API with my username and wrong event id")
def step_impl(context):
    headers = {
        'Authorization':'Token '+ context.key
    }

    resp = requests.get(context.test.live_server_url + "/host/qa/eventwise_qas/?event_id=30", headers=headers)
    assert resp.status_code >= 400

    context.api_response_data = resp.json()


@then("I expect the empty list of questions in response because the event id doesn't exist")
def step_impl(context):
    assert context.api_response_data["message"] == "The event ID that you've entered is not in the records"


@given("that I am a registered host of privilege walk and wants to get questions without giving event id")
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



@when("I make an API call to get questions API with my username and without event id")
def step_impl(context):
    headers = {
        'Authorization':'Token '+ context.key
    }

    resp = requests.get(context.test.live_server_url + "/host/qa/eventwise_qas/", headers=headers)
    assert resp.status_code >= 400

    context.api_response_data = resp.json()


@then("I expect the empty list of questions in response because the event id is missing")
def step_impl(context):
    assert context.api_response_data["message"] == "Please enter an event ID"

