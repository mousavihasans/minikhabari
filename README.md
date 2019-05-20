# minikhabari
A test project for crawling news! At the first phase, I focus on isna.ir

### Project stack:
* Django
* SQLite (It is not appropriate for production!)
* celery
* redis

### Setup Project:


```
pip install -r requirements.txt
```


* redis must be installed and run in port 6379.
* celery must be installed and run using the followin command (this is not proper for production):
```
celery -A minikhabari worker -l info -B
```
