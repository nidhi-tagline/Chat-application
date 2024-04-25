# Chat-application
This is simple chat application built with Django, Django-channels and Redis. Application has functionalities like user authentication, creating a room, joining a room, sending messages, and viewing messages.

## Installation
1. Clone the repository
```bash
git clone https://github.com/nidhi-tagline/Chat-application.git
```

2. Navigate to project directory 
```bash
cd ChatApplication
```

3. Create a virtual environment and activate it
```bash
python3 -m venv env
source env/bin/activate
```

4. Install the Dependencies:
```bash
(env)$ pip install -r requirements.txt
```

5. Make migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

6. run redis server
```bash
redis-server
```
or using docker
```bash
docker run -p 6379:6379 -d redis:5
```

7. Runserver
```bash
python3 manage.py runserver
```

8. Open http://localhost:8000 in your browser