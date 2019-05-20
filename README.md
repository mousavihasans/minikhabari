# minikhabari
A test project for crawling news! At the first phase, I focus on isna.ir

### Project stack:
* Python 3.6
* Django 2.2
* SQLite (It is not appropriate for production!)
* Celery 4.3
* Redis 3.2
* Requests 2.9
* Beautifulsoup 4.7

### Setup Project:


```
pip install -r requirements.txt
```

* Do not forget to create vritualenv!
* Redis must be installed and run in port 6379.
* Celery must be installed and run using the followin command (this is not proper for production):
```
celery -A minikhabari worker -l info -B
```

### Todo:
* Fix some problems in parsing tags and tables and videos
* Add more tests
* Dockerize the project