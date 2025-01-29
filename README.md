## User Guide 
This is a real-time chat application built using Django. 
It allows users to send and receive messages in real-time through websockets. 
It provides an intuitive interface and supports multiple users.

## Features
- Real-time messaging with WebSocket support
- User authentication (login/signup)
- Chat rooms (One-to-One relationship)
- Responsive UI

## Requirements
- Python 3.10 or higher
- Django 3.8 or higher
- Channels (for WebSockets)
- Redis (for Channels layer)
- Daphne (It acts as the interface between your Django application and the outside world, specifically in scenarios where you are handling asynchronous requests, such as WebSocket connections.)

## Installation
Follow the steps below to set up and run the project locally:

### 1. Clone the repository
```bash
git clone https://github.com/91kotte/django_chatApplication.git
cd django_chatApplication
```

### 2. Create a virtual environment

It's recommended to use a virtual environment to manage your dependencies. You can create one by running:

```bash or teminal
python3 -m venv venv
```

Activate the virtual environment:
- On Windows:
  ```bash or teminal
  venv/Scripts/activate
  ```
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### 3. Install the dependencies
Install the required dependencies using `pip`:

```bash or teminal
pip install -r requirements.txt
```

### 5. Apply migrations
Run Django migrations to set up the database schema:

```bash or teminal
python manage.py migrate
```

### 6. Create a superuser (optional)

If you want to access the Django admin panel, create a superuser:

```bash or teminal
python manage.py createsuperuser
```

### 7. Run the development server
Finally, run the Django development server:

```bash or teminal
python manage.py runserver
```

Now, you can visit your chat application at `http://127.0.0.1:8000` in your web browser.

## Usage
- Upon opening the URL, you will be directed to the login page. If you already have an account, log in; otherwise, register a new account.
- After logging in, you'll see a list of all registered users on the left panel under the **"Chats"** section.
- To start a conversation, simply click on any user from the **"Chats"** list.
- Clicking on a user's name will open the corresponding chatroom beside the left panel, where you can interact with that user.
- Send and receive messages in real-time.
- If desired, you can collapse the chat list by clicking on the arrow icon before the user's name in the chat room on top, located in the main content area.
- To log out, click the **"Logout"** option located in the top right corner of the navbar.


### Notes:
- **WebSocket support**: If your chat app uses Django Channels for real-time communication, ensure that your `requirements.txt` includes the necessary packages, like `channels` and `channels_redis`.
- **Redis setup**: Redis is required for Django Channels to manage WebSockets. Make sure to explain how to install and run Redis if your app depends on it.
