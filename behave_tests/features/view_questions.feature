# Created by sindhuja at 3/27/22
Feature: View questions and answers
  Question answer related APIs demonstration using the get questions API

  Scenario: The host can get questions and answer choices to existing event
    Given that I am a registered host of privilege walk events and want to get questions and answer choices for the event
      When I make an API call to get questions API with my correct username and correct eventid
      Then I expect the response that gives the list of questions and answer choices related to that event

  Scenario: The host can get empty list of questions and answer choices if there are no questions created for that event
    Given that I am a registered host of privilege walk and wants to get questions for the event that has no questions added to it
      When I make an API call to get questions API with my username and event id
      Then I expect the empty list of questions in response
    
  Scenario: The host can get empty list of questions and answer choices if the given event id doesn't exist
    Given that I am a registered host of privilege walk and wants to get questions by giving wrong event id 
      When I make an API call to get questions API with my username and wrong event id
      Then I expect the empty list of questions in response because the event id doesn't exist

  Scenario: The host can get empty list of questions and answer choices if the event id is missing in request
    Given that I am a registered host of privilege walk and wants to get questions without giving event id 
      When I make an API call to get questions API with my username and without event id
      Then I expect the empty list of questions in response because the event id is missing
