# Websocket Documentation
This will contain different types of Websockets and how to use them, along with sample requests and responses. If you're building Websockets, please make sure you update this documentation on how to use that Websocket. The easiest way to do this would be to copy, paste and edit the 1st Websocket in this doc.

# Walk Event - Question and Answer control
This channel can be used during the privilege walk event. The event ID will be used as the room ID

**URL endpoint:** `/ws/walk/qa_control/<event_id>/`

## Basic overview
### As a host:

You can get:
1. Active user count
2. Number of users who have responded to the question displaying

You can send:
1. An order to move to the next question in the list

### As a participant:

You can get:
1. Active user count
2. Number of users who have responded to the question displaying
3. An order to move to the next question in the list

You can send:
1. Your answer choice (id)


## 1. Active user count
Meant for everyone to get to know the number of users who are currently active in the session.

_**Type:**_ Receivable message
### Format
```angular2html
{
    "meant_for": "all",
    "type": "active_user_count",
    "data": {
        "n_active_users": 12
    }
}
```

## 2. Responded user count
Meant for everyone connected to the room to get to know the number of users who have responded to the question being showed

_**Type:**_ Receivable message
### Format
```angular2html
{
    "meant_for": "all",
    "type": "answer_count",
    "data": {
        "n_users_answered": 25,
        "increment_answer_id": 15
    }
}
```

## 3. Next question order (Host side)
Meant for the host to tell all the participants to move to the next question

_**Type:**_ Sendable message
### Format
```angular2html
{
    "type": "question_move"
}
```

## 4. Next question order (Participant side)
Meant for the participants to move to the next question

_**Type:**_ Receivable message
### Format
```angular2html
{
    "meant_for": "participants",
    "type": "question_move",
}
```

## 5. Answer Choice
Meant for the participants to send their answer choice for a particular question

_**Type:**_ Sendable message
### Format
```angular2html
{
    "type": "answer_choice",
    "data": {
        "participant_code": "ABCDXYZ",
        "answer_choice_id": 611
    }
}
```

## 6. Line position graph values
The host will receive this after a participant would answer a question in the event. This should be used by the host to update the lines and the count of users on each of the lines on the graph displayed on the front end.

_**Type:**_ Receivable message
### Format
```angular2html
{
    "meant_for": "host",
    "type": "line_counts",
    "data": {
        "position_stats": {
            "-22": 1,
            "-1": 1
        }
    }
}
```

The key in the `position_stats` represents the line number and the corresponding value represents the number of people on that particular line.
