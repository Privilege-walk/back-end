# Created by sindhuja at 3/27/22
Feature: Create questions and answers
  Question answer related APIs demonstration using the create questions API

#  Scenario: The host can add questions and answer choices to existing event
#    Given that I am a registered host of privilege walk events and want to create questions and answer choices for the event
#      When I make an API call to create questions API with my correct username, questions, answer choices and correct eventid
#      Then I expect the response that gives the status and id of the created question

#  Scenario: The host fails to create questions and answer choices because of incorrect eventid
#    Given that I am a registered host of privilege walk and wants to create questions but with wrong eventid
#      When I make an API call to create questions API with my username, questions, answer choices and wrong event id
#      Then I expect the response that says questions cannot be created as event id doesn't exist
    
#  Scenario: The host fails to create questions and answer choices because of missing eventid
#    Given that I am a registered host of privilege walk and wants to create questions but without giving eventid
#      When I make an API call to create questions API with my username, questions, answer choices and without event id
#      Then I expect the response that says questions cannot be created as event id is missing

  Scenario: The host fails to create question and answer choices because of authentication failure
    Given that I am a registered host of privilege walk events and want to create questions but forgets to give username 
      When I make an API call to create questions API with missing username in request
      Then I expect the response that says questions cannot be created and username is required in request