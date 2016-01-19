## Scholarly Citation Finder

#### Setup

Install Python dependencies
```
pip install -r requirements.txt
```

Create database
```
sudo -u postgres createdb mag
```

Migrate databases
```
python manage.py migrate --database=NAME
```

Run server: `make run`

#### Set environment variables

Available environment variables:
* MAG database: `MAG_DATABASE_NAME`, `MAG_DATABASE_USER`, `MAG_DATABASE_PASSWORD`

Set an environment variable:
* Linux: `export <variable-name>=<value>`
** Store it via: `echo "export <variable-name>=<value>" >> ~/.bashrc`
* Windows: `SET <variable-name>=<value>`

#### Shell

Open a shell for testing or debuggin
```
python manage.py shell
>>> import django
>>> django.setup()
>>> SOME ACTION HERE
```

#### Code style
 
Style convention: [PEP 8](https://www.python.org/dev/peps/pep-0008/).

Tool: [pep8 ](https://pypi.python.org/pypi/pep8) with the param `--ignore=E265,E501,W293` (E265 _block comment should start with ‘# ‘_, E501 _line too long_, W293 _blank line contains whitespace_)