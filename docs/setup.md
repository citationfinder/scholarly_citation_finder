<h1>Setup</h1>

## Setup for local development

It's recommanded to create a virtual Python environment, but not required. Therefore create and activate it.
```bash
$ virtualenv scf_project
$ cd scf_project/
$ source bin/activate
```

### Setup server

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

Create a root user
```bash
$ ./manage.py createsuperuser
```

Start Celery
```bash
$ celery -A scholarly_citation_finder worker -l info
```

Finally run the build-in Django server
```bash
$ ./manage.py runserver
```

Open [http://localhost:8000](http://localhost:8000)

### Setup client

The client is located in the `public/client` directory. Gulp in combination with Webpack is used to build the client. During development run Gulp to automatically build the project and reload the browser, when you change files

```bash
$ cd public/client
$ gulp
```

Open [http://localhost:4000](http://localhost:4000)


### Documenation

MkDocs is used for this documentation. Run MkDocs during writing to check the results

```bash
$ mkdocs serve
```

Open [http://localhost:8000](http://localhost:8000)


## Setup a virtual machine

see [Deploy Vagrant](deployment.md)