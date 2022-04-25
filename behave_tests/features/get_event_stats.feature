# Created by sindhuja at 3/27/22
#Feature: Get events statistics
#  Event statistics related APIs demonstration using the get event statistics API

#  Scenario: The host gets the statistics of event results
#    Given that I am a registered host of privilege walk events and want to see the event statistics
#      When I make an API call to the get event statistics API with event id
#      Then I expect the response that gives the list of bars and number of participants standing on the bars

#  Scenario: The participant gets the statistics of event results and participant location
#    Given that I am a participant of privilege walk events and want to see the event statistics and my location
#      When I make an API call to the get event statistics API with event id and participant unique code
#      Then I expect the response that gives the list of bars and number of participants standing on the bars and my location

#  Scenario: The host gets error message when event id is not valid
#    Given that I am a registered host of privilege walk events and gave wrong event id
#      When I make an API call to the get event statistics API with wrong event id
#      Then I expect the response that says event id doesn't exists

#  Scenario: The participant gets error message when unique code is not valid
#    Given that I am a participant of privilege walk event and forgot my unique code
#      When I make an API call to the get event statistics API with wrong unique code
#      Then I expect the response that says unique code doesn't exists