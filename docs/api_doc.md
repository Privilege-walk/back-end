# API Documentation
This will contain different types of APIs and how to use them, along with sample requests and responses. If you're building an API, please make sure you update this documentation on how to use that API. The easiest way to do this would be to copy, paste and edit the 1st API in this doc.

# Authentication APIs
## 1. Sign Up (Host sign up)
### Description
This API can be called to sign a user up as a  privilege walk host.
<table>
<tr>
    <td>Endpoint</td>
    <td>Method</td>
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
    <td>Endpoint</td>
    <td>Method</td>
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
    <td>Endpoint</td>
    <td>Method</td>
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
    <td>Endpoint</td>
    <td>Method</td>
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
    "name": "The event's title goes here"
}
```

### Sample Output
```angular2html
{
    "status": "created",
    "id": 890
}
```