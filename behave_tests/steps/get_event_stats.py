# from behave import *
# import requests

# from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token

# use_step_matcher("re")

# @given("that I am a registered host of privilege walk events and want to see the event statistics")
# def step_impl(context):
#     context.username = "12thMan"
#     context.password = "SomePassword123"
#     context.first_name = "12th"
#     context.last_name = "Man"
#     context.email = "twelve@testtamu.edu"

#     usr = User.objects.create_user(
#         context.username,
#         context.email,
#         context.password
#     )
#     usr.first_name = context.first_name
#     usr.last_name = context.last_name
#     usr.save()

#     registered_user = User.objects.filter(username="12thMan")

#     assert len(registered_user) == 1

#     user_auth_token, _ = Token.objects.get_or_create(user=usr)
#     context.key = user_auth_token.key

#     data = {
#         "name": "New year event"
#     }
#     headers = {
#         'Authorization':'Token '+ context.key
#     }

#     resp = requests.post(context.test.live_server_url + "/host/events/create/", data, headers=headers)

#     context.event_api_response_data = resp.json()
#     context.eventId = context.event_api_response_data["id"]
#     data = {
#         "event_id": context.eventId,
#         "title": "The question's title goes here",
#         "choices": [
#             {
#                 "description": "Pizza",
#                 "value": 1
#             },
#             {
#                 "description": "Ice Cream",
#                 "value": 2
#             },
#             {
#                 "description": "Salt Water",
#                 "value": -1
#             }
#         ]
#     }
#     headers = {
#         'Authorization':'Token '+ context.key
#     }

#     resp = requests.post(context.test.live_server_url + "/host/qa/create/", data, headers=headers)

#     data = {
#         "event_id": context.eventId
#     }
#     headers = {
#         'Authorization':'Token '+ context.key
#     }

#     resp = requests.post(context.test.live_server_url + "/walk/register_participant/", data, headers=headers)

#     # Response.


# @when("I make an API call to the get events API with my correct username")
# def step_impl(context):
#     headers = {
#         'Authorization':'Token '+ context.key
#     }

#     resp = requests.get(context.test.live_server_url + "/host/events/all/", headers=headers)
#     assert resp.status_code >= 200 and resp.status_code < 300

#     context.api_response_data = resp.json()


# @then("I expect the response that gives the list of events on my username as host")
# def step_impl(context):
#     assert context.api_response_data["events"][0]["name"] == "New year event"