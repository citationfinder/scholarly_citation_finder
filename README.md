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
* Databases: `<name>_DATABASE_NAME`, `<name>_DATABASE_USER`, `<name>_DATABASE_PASSWORD`

Set an environment variable:
* Linux: `export <variable-name>=<value>`
    * Store it via: `echo "export <variable-name>=<value>" >> ~/.bashrc`
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

## Harvester

### MAG

```
cd downloads/harvester/mag
curl -O https://academicgraph.blob.core.windows.net/graph-2015-11-06/MicrosoftAcademicGraph.zip
7z x MicrosoftAcademicGraph.zip
```
