# Created by sindhuja at 3/12/22
Feature: Sign Up new user
  Signing up a new user demonstration using the sign up API as example

  Scenario: The user signs up successfully
    Given that I am a unregistered host of privilege walk events
      When I make an API call to the sign up API with my details
      Then I expect the response to tell me that I have signed up successfully
  
  Scenario: The user sign up is unsuccessful due to email id already used
    Given that I am someone who wants to signup with used emailid
      When I make an API call to the sign up API with a used email id
      Then I expect the response to tell me that the sign up is not successful due to email id is already used

  Scenario: The user sign up is unsuccessful due to username already used
    Given that I am someone who wants to signup with used username
      When I make an API call to the sign up API with a used username
      Then I expect the response to tell me that the sign up is not successful due to username is already used