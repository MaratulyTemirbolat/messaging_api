# API for Message sending through Telegram
## Project Description
This API is aimed to obtain messages as requests and duplicate them through the user's telegram which is connected to api.

## Api End points

### Registration
URL: http://localhost:8000/api/v1/auths/users/register_user
Required data: login: string, first_name: string, password: string
Method: POST
Permissions: Any person

### Login
URL: http://localhost:8000/api/v1/auths/users/login_user
Required data: login: string, password: string
Method: POST
Persmissions: Any person

### Get user messages
URL: http://localhost:8000/api/v1/auths/users/messages
Required data: No
Method: GET
Required Headers: Authorization (JWT YOUR_TOKEN)
Permissions: Authenticated person

### Get telegram token
URL: http://localhost:8000/api/v1/auths/users/get_token
Required data: No
Method: GET
Required Headers: Authorization (JWT YOUR_TOKEN)
Persmissions: Authenticated person

### Upload message
URL: http://localhost:8000/api/v1/chats/messages/upload_message
Required data: No
Method: POST
Required Headers: Authorization (JWT YOUR_TOKEN)
Permissions: Authenticated person

## Install requirements
pip install -r tools/requirements.txt

## Migrations

### Create Migrations

For Linux: python3 manage/local.py makemigrations
For Windows: python manage/local.py makemigrations

### Apply migrations

For Linux: python3 manage/local.py migrate
For Windows: python manage/local.py migrate

## Collect Static

For Linux: python3 manage/local.py collectstatic
For Windows: python manage/local.py collectstatic