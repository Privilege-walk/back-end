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