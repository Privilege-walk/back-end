from behave import *
import requests

from django.contrib.auth.models import User

use_step_matcher("re")


@given("that I am a unregistered host of privilege walk events")
def step_impl(context):
    context.username = "12thMan"
    context.password = "SomePassword123"
    context.first_name = "12th"
    context.last_name = "Man"
    context.email = "twelve@testtamu.edu"


@when("I make an API call to the sign up API with my details")
def step_impl(context):
    data = {
        "username": context.username,
        "password": context.password,
        "email" : context.email,
        "first_name" : context.first_name,
        "last_name" : context.last_name
    }

    resp = requests.post(context.test.live_server_url + "/auth/signup/", data)
    assert resp.status_code >= 200 and resp.status_code < 300

    context.api_response_data = resp.json()


@then("I expect the response to tell me that I have signed up successfully")
def step_impl(context):
    assert context.api_response_data["created"] == "success"



@given("that I am someone who wants to signup with used emailid")
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


@when("I make an API call to the sign up API with a used email id")
def step_impl(context):
    data = {
        "username": context.username,
        "password": context.password,
        "email" : context.email,
        "first_name" : context.first_name,
        "last_name" : context.last_name
    }

    resp = requests.post(context.test.live_server_url + "/auth/signup/", data)
    assert resp.status_code >= 200 and resp.status_code < 300

    context.api_response_data = resp.json()


@then("I expect the response to tell me that the sign up is not successful due to email id is already used")
def step_impl(context):
    assert context.api_response_data["created"] == "email exists"

@given("that I am someone who wants to signup with used username")
def step_impl(context):
    context.username = "12thMan"
    context.password = "SomePassword123"
    context.first_name = "12th"
    context.last_name = "Man"
    context.email = "different@testtamu.edu"

    usr = User.objects.create_user(
        context.username,
        "twelve@testtamu.edu",
        context.password
    )
    usr.first_name = context.first_name
    usr.last_name = context.last_name
    usr.save()

    registered_user = User.objects.filter(username="12thMan")

    assert len(registered_user) == 1


@when("I make an API call to the sign up API with a used username")
def step_impl(context):
    data = {
        "username": context.username,
        "password": context.password,
        "email" : context.email,
        "first_name" : context.first_name,
        "last_name" : context.last_name
    }

    resp = requests.post(context.test.live_server_url + "/auth/signup/", data)
    assert resp.status_code >= 200 and resp.status_code < 300

    context.api_response_data = resp.json()


@then("I expect the response to tell me that the sign up is not successful due to username is already used")
def step_impl(context):
    assert context.api_response_data["created"] == "username exists"