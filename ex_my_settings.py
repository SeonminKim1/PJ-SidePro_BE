MYSQL_DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<your schema name>', # Schema Name
        'USER': '<your username>', # USER NAME
        'PASSWORD': '<your password>', # PASSWORD NAME
        'HOST':'127.0.0.1',
        'PORT':'3306',
    }
}

POSTGRESQL_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<your schema name>', # Schema Name
        'USER': 'postgres',
        'PASSWORD': '<your password>', # PASSWORD NAME
        'HOST':'127.0.0.1',
        'PORT':'5432',
    }
}

SECRET_KEY = '<your django key>'
