<h1>Setup</h1>

## Setup for local development

It's recommanded to create a virtual Python environment, but not required. Therefore create and activate it.
```bash
$ virtualenv scf_project
$ cd scf_project/
$ source bin/activate
```

Get SCF and install the Python dependencies
```bash
$ git clone https://github.com/citationfinder/scholarly_citation_finder.git
$ cd scholarly_citation_finder
$ pip install -r requirements.txt
```

Migrate the database tables and collect the static files
```bash
$ ./manage.py migrate
$ ./manage.py collectstatic
```

Start Celery
```bash
$ celery -A scholarly_citation_finder worker -l info
```

Finally run the build-in Django server
```bash
$ ./manage.py runserver
```

### Django tips

Migrate a specific database or flush it
```bash
$ ./manage.py migrate --database=<database name>
$ ./manage.py flush --database=<database name>
```

Open Django shell for testing or debugging
```bash
$ python manage.py shell
>>> import django
>>> django.setup()
```


### PostgreSQL tips

Open PostgreSQL shell
```bash
$ psql -U <user name> [<database name>]
```

Create a user and a database
```
CREATE USER <username> WITH PASSWORD '<password>';
CREATE DATABASE <name> [OWNER <username>];
```