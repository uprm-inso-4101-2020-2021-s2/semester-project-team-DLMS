# UPR-Grader

## Setup

- pip install psycopg2
- Install postgreSQL to your PC: https://www.postgresql.org/download/ version 13.1
- Make sure when installing to check pgAdmin 4 (Should be checked automatically)

## TODO: DB Setup IMPORTANT

- **WORK-IN-PROGRESS** (WIP)


## DB Table Updates
1. ```python manage.py makemigrations UPR_Grader```
2. ```python manage.py migrate```

## Testing DB Connection
1. Go to UPR_Grader/views.py and uncomment ```def queries_test(request)```
2. Add this to IntroProject/urls.py: ```path('', include('UPR_Grader.urls')),```
3. Add this to UPR_Grader/urls.py: ```path('test/', views.queries_test, name='TEST'),```
4. Run app, go to url: http://127.0.0.1:8000/test/ and this should pop up if an object was added: Students object (1)