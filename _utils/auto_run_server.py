import os
os.system('python manage.py makemigrations chat project user')
os.system('python manage.py migrate')
os.system('python manage.py runserver')