# API Documentation
This will contain different types of APIs and how to use them, along with sample requests and responses. If you're building an API, please make sure you update this documentation on how to use that API. The easiest way to do this would be to copy, paste and edit the 1st API in this doc.

# Authentication APIs
## 1. Sign Up (Host sign up)
### Description
This API can be called to sign a user up as a  privilege walk host.
<table>
<tr>
    <th>Endpoint</th>
    <th>Method</th>
</tr>
<tr>
    <td>/auth/signup/</td>
    <td>POST</td>
</tr>
</table>

### Input data
Note: Type can either be JSON, URL parameters, or anything else that can be taken in as input.

**Type:** JSON

**Sample Input:**
```angular2html
{
    "username": "acoolsomebody",
    "password": "CoolFolks12345!",
    "first_name": "Jon",
    "last_name": "Doe",
    "email": "jondoe@yahoo.com"
}
```

### Response data
**Type:** JSON

**Sample Response (user creation successful):**
```angular2html
{
    "created": "success"
}
```

**Sample Response (user creation unsuccessful):**
This could be because the username or the email already exists

```angular2html
{
    "created": "username exists"
}
```
```angular2html
{
    "created": "email exists"
}
```

## 2. Log In (Host Login)
### Description
<table>
<tr>
    <th>Endpoint</th>
    <th>Method</th>
</tr>
<tr>
    <td>/auth/login/</td>
    <td>POST</td>
</tr>
</table>

### Input data

**Type:** JSON

**Sample Input:**
```angular2html
{
    "username": "acoolsomebody",
    "password": "CoolFolks12345!"
}
```

### Response data
**Type:** JSON

**Sample Response (user creation successful):**
```angular2html
{
    "status": true,
    "token": "123bkjbajksbdjkab12bek1b"
}
```

**Sample Response (user creation unsuccessful):**

```angular2html
{
    "status": false
}
```

# Event APIs
## 1. Get all events
### Description
This API can be called on the main dashboard page to get all the events created by a particular host (typically, the host who has logged in).

<table>
<tr>
    <th>Endpoint</th>
    <th>Method</th>
</tr>
<tr>
    <td>/host/events/all/</td>
    <td>GET</td>
</tr>
</table>

### Input data
**Type:** JSON
#### Request Header:
```angular2html
{
    "Authorization": "Token <whatever_the_host's_token_is>"
}
```
#### Request Body:
Not required

### Sample Output
```angular2html
{
    "events": [
        {
            "id": 123,
            "name": "Halloween",
            "status": "Created"
        },
        {
            "id": 456,
            "name": "New Year",
            "status": "Running"
        },
        {
            "id": 789,
            "name": "Orientation",
            "status": "Ended"
        }
    ]
}
```

## 2. Create Event
### Description
This API can be called to create an event. The host will be set as the user whose token is provided in the auth section of the request header.

<table>
<tr>
    <th>Endpoint</th>
    <th>Method</th>
</tr>
<tr>
    <td>/host/events/create/</td>
    <td>POST</td>
</tr>
</table>

### Input data
**Type:** JSON
#### Request Header:
```angular2html
{
    "Authorization": "Token <whatever_the_host's_token_is>"
}
```
#### Request Body:
```angular2html
{
    "name": "The event's title goes here",
    "x_label_min": "Some text to be displayed on the graph",
    "x_label_max": "Something else you want to be displayed on the graph"
}
```

### Sample Output
```angular2html
{
    "status": "created",
    "id": 890
}
```

# Question and answer APIs
## 1. Create Question
### Description
This API can be used to create a question by specifying what the question is, the answer choices, and the move points for each answer choice.

<table>
<tr>
    <th>Endpoint</th>
    <th>Method</th>
</tr>
<tr>
    <td>/host/qa/create/</td>
    <td>POST</td>
</tr>
</table>

### Input data
**Type:** JSON
#### Request Header:
```angular2html
{
    "Authorization": "Token <whatever_the_host's_token_is>"
}
```
#### Request Body:
```angular2html
{
    "event_id": 123,
    "title": "The question's title goes here",
    "choices": [
        {
            "description": "Pizza",
            "value": 1
        },
        {
            "description": "Ice Cream",
            "value": 2
        },
        {
            "description": "Salt Water",
            "value": -1
        }
    ]
}
```

### Sample Output
```angular2html
{
    "status": "created",
    "id": 456
}
```


## 2. View all questions (Event details)
### Description
This can be used to view all the questions and the answers available for each question for a particular event

<table>
<tr>
    <th>Endpoint</th>
    <th>Method</th>
</tr>
<tr>
    <td>/host/qa/eventwise_qas/</td>
    <td>GET</td>
</tr>
</table>

### Input data
**Type:** JSON
#### Request Header:
```angular2html
{
    "Authorization": "Token <whatever_the_host's_token_is>"
}
```
#### Request Body:
Not Required

#### URL Parameters:
Ex: `base_url.tld/endpoint/goes_here/?parameter_1=xxx&parameter_2=yyy`

<table>
<tr>
    <th>Parameter</th>
    <th>Example Value</th>
</tr>
<tr>
    <td>event_id</td>
    <td>123</td>
</tr>
</table>

### Sample Output
```angular2html
{
    "event_id": 123,
    "name": "Party",
    "status": "created",
    "x_label_min": "Some text to be displayed on the graph",
    "x_label_max": "Something else you want to be displayed on the graph",
    "questions": [
        {
            "id": 890,
            "description": "The Question content",
            "choices": [
                {
                    "id": 876,
                    "description": "Pizza",
                    "value": 1
                },
                {
                    "id": 54,
                    "description": "Ice Cream",
                    "value": 2
                },
                {
                    "id": 89,
                    "description": "Salt Water",
                    "value": -1
                },
                .
                .
                .
            ]
        },
        .
        .
        .
    ]
}
```

* `questions` will contain the list of all the questions within the event.
* Each of the object within `questions` will represent a question and will contain a list of answer choice objects within a list called `choices`.


# Walk event APIs
## 1. Register participant
### Description
This API can be used to register a participant as an anonymous participant and get the participant code for them.

<table>
<tr>
    <th>Endpoint</th>
    <th>Method</th>
</tr>
<tr>
    <td>/walk/register_participant/</td>
    <td>POST</td>
</tr>
</table>

### Input data
**Type:** JSON

#### Request Body:
```angular2html
{
    "event_id": 123
}
```

### Sample Output (success)
```angular2html
{
    "status": "registered",
    "participant_code": "ABCDXYZ"
}
```

### Sample Output (failure)
```angular2html
{
    "message": "<details of the failure>"
}
```

# Results Page APIs
## 1. View question and response statistics
### Description
This can be used to view the questions, answer choices and number of participants chosen that corresponding answer choice for a particular event

<table>
<tr>
    <th>Endpoint</th>
    <th>Method</th>
</tr>
<tr>
    <td>/host/qa_stats/</td>
    <td>GET</td>
</tr>
</table>

### Input data
**Type:** JSON
#### Request Header:
```angular2html
{
    "Authorization": "Token <whatever_the_host's_token_is>"
}
```
#### Request Body:
Not Required

#### URL Parameters:
Ex: `base_url.tld/endpoint/goes_here/?parameter_1=xxx&parameter_2=yyy`

<table>
<tr>
    <th>Parameter</th>
    <th>Example Value</th>
</tr>
<tr>
    <td>event_id</td>
    <td>123</td>
</tr>
</table>

### Sample Output
```angular2html
[
    {
        "question_id": 1,
        "question": "Are you above 18?",
        "answers": [
            {
                "answer_id": 1,
                "answer": "Yes",
                "count": 2
            },
            {
                "answer_id": 2,
                "answer": "No",
                "count": 2
            }
        ]
    },
    {
        "question_id": 2,
        "question": "Do you like sweets?",
        "answers": [
            {
                "answer_id": 3,
                "answer": "Yes",
                "count": 3
            },
            {
                "answer_id": 4,
                "answer": "No",
                "count": 1
            }
        ]
    },
        .
        .
        .
]
```

* `answers` will contain the list of all the answer choices for the question and count of participants who chosen the corresponding answer choice within the event.

## 2. View Event statistics (for bar graph)
### Description
This can be used to view the line locations and number of participants standing in that particular line

<table>
<tr>
    <th>Endpoint</th>
    <th>Method</th>
</tr>
<tr>
    <td>/host/event_stats/</td>
    <td>GET</td>
</tr>
</table>

### Input data
**Type:** JSON
#### Request Header:
```angular2html
{
    "Authorization": "Token <whatever_the_host's_token_is>"
}
```
#### Request Body:
Not Required

#### URL Parameters:
Ex: `base_url.tld/endpoint/goes_here/?parameter_1=xxx&parameter_2=yyy`

<table>
<tr>
    <th>Parameter</th>
    <th>Example Value</th>
</tr>
<tr>
    <td>event_id</td>
    <td>123</td>
</tr>
<tr>
    <td>unique_code</td>
    <td>HOAQ</td>
</tr>
</table>

### Sample Output
```angular2html
{
    "barDefaultColor": "#8884d8",
    "xLabelMin": "Some text to be displayed on the graph",
    "xLabelMax": "Something else you want to be displayed on the graph",
    "data": [
        {
            "barName": "",
            "count": 1,
            "participantLocation": false
        },
        {
            "barName": "",
            "count": 1,
            "participantLocation": false
        },
        {
            "barName": "",
            "count": 2,
            "participantLocation": true
        },
        .
        .
        .
    ]
}
```

* `data` will contain the list of bars and count of participants standing on the bar by the end of the event.
