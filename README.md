# API for Message sending through Telegram

<hr/>

## Project Description
This API is aimed to obtain messages as requests and duplicate them through the user's telegram which is connected to api.

<hr/>

## Api End points

### Registration
URL: http://localhost:8000/api/v1/auths/users/register_user <br/>
Required data: login: string, first_name: string, password: string <br/>
Method: POST <br/>
Permissions: Any person <br/>

### Login
URL: http://localhost:8000/api/v1/auths/users/login_user <br/>
Required data: login: string, password: string <br/>
Method: POST <br/>
Persmissions: Any person <br/>

### Get user messages
URL: http://localhost:8000/api/v1/auths/users/messages <br/>
Required data: No  <br/>
Method: GET  <br/>
Required Headers: Authorization (JWT YOUR_TOKEN)  <br/>
Permissions: Authenticated person  <br/>

### Get telegram token
URL: http://localhost:8000/api/v1/auths/users/get_token  <br/>
Required data: No  <br/>
Method: GET  <br/>
Required Headers: Authorization (JWT YOUR_TOKEN)  <br/>
Persmissions: Authenticated person  <br/>

### Upload message
URL: http://localhost:8000/api/v1/chats/messages/upload_message  <br/>
Required data: No  <br/>
Method: POST  <br/>
Required Headers: Authorization (JWT YOUR_TOKEN)  <br/>
Permissions: Authenticated person  <br/>

<hr/>

## Install requirements
pip install -r tools/requirements.txt

<hr/>

## Migrations

### Create Migrations

For Linux: python3 manage/local.py makemigrations
For Windows: python manage/local.py makemigrations

### Apply migrations

For Linux: python3 manage/local.py migrate
For Windows: python manage/local.py migrate

<hr/>

## Static

### Collect project static

For Linux: python3 manage/local.py collectstatic
For Windows: python manage/local.py collectstatic