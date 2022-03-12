# Created by surajsjain at 3/11/22
Feature: Login authentication
  Authentication APIs demonstration using the login API as example

  Scenario: The host logs in successfully
    Given that I am a registered host of privilege walk events
      When I make an API call to the login API with my correct username and password
      Then I expect the response to tell me that I have logged in successfully
      And Also give me a token that I can use in the future to authenticate to the back-end