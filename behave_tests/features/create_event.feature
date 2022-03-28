# Created by sindhuja at 3/27/22
Feature: Create events
  Event related APIs demonstration using the create events API

  Scenario: The host can create a event
    Given that I am a registered host of privilege walk events and want to create a event
      When I make an API call to create event API with my correct username
      Then I expect the response that gives the status and id of the created event

  Scenario: The host fails to create a event if the username doesn't exist in the system
    Given that I am not a registered host of privilege walk and wants to create a event
      When I make an API call to create event API with my unregistered username
      Then I expect the response that says event cannot be created and user has to be registered

  Scenario: The host fails to create a event if the username is missing in request
    Given that I am a registered host of privilege walk events and want to create a event but forgets to give username 
      When I make an API call to create event API with missing username in request
      Then I expect the response that says event cannot be created and username is required in request