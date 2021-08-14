# live-session-scheduler

### How to run

Create a virtual environment and activate 

```
python3 -m venv myvenv
cd myvenv 
source ./bin/activate
```

Clone this repository

```
git clone https://github.com/patricechaula/live-session-scheduler.git
cd live-session-scheduler
pip install -r requirements.txt
```

Apply migrations
```
python manage.py migrate
```

Create super user
```
python manage.py createsuperuser
```

Run

```
python manage.py runserver
```


