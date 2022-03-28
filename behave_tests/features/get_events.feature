# Created by sindhuja at 3/27/22
Feature: Get events
  Event related APIs demonstration using the get events API

  Scenario: The host gets the list of events created
    Given that I am a registered host of privilege walk events and exists events on my username
      When I make an API call to the get events API with my correct username
      Then I expect the response that gives the list of events on my username as host

  Scenario: The host gets the empty list if no events with my username
    Given that I am a registered host of privilege walk events and there exists no events on my username
      When I make an API call to the get events API with my username
      Then I expect the response that gives the empty list as response

  Scenario: The host gets the empty list if my username is wrong
    Given that I am a registered host of privilege walk events and forgot my username
      When I make an API call to the get events API with wrong username
      Then I expect the response that says username doesn't exists