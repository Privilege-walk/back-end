# Created by sindhuja at 4/9/22
Feature: register new participant
  participant's registration demonstration using the participant registration API as example

  Scenario: The participant registers successfully
    Given that I am a unregistered participant of a event
      When I make an API call to the participant registration API with event id
      Then I expect the response to tell me the re is successful and give a participant code
  
  Scenario: The participant registration is unsuccessful when event id is missing
    Given that I am a participant and wants to join an event and forgets to give event id
      When I make an API call to the participant registration API without giving event id
      Then I expect the response to tell me that the registration is not successful

  Scenario: The participant registration is unsuccessful when event id is wrong
    Given that I am a participant and want to join an event by giving wrong event id
      When I make an API call to the participant registration API with wrong event id
      Then I expect the response to tell me that the registration is not successful and event id is wrong