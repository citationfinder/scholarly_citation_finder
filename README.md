## Scholarly Citation Finder

#### Repositories

* [search-for-citations](https://sun01.pool.ifis.uni-luebeck.de/groppe/search-for-citations) Source code of the web service
    * [thesis](https://sun01.pool.ifis.uni-luebeck.de/rosenthal/search-for-citations-thesis) LaTex source files and cited papers of the thesis
    * [deployment](https://sun01.pool.ifis.uni-luebeck.de/rosenthal/search-for-citations-deployment) Deployment scripts of the web serivce
    * [dataset](https://sun01.pool.ifis.uni-luebeck.de/rosenthal/search-for-citations-dataset) Data sets for testing 
* [publin](https://github.com/CiteEt/publin) Fork to integrate citation support
* ... further repos on [github.com/CiteET](https://github.com/CiteET)

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
* DBLP database: `DBLP_DATABASE_NAME`, `DBLP_DATABASE_USER`, `DBLP_DATABASE_PASSWORD`

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

## Harvester

### MAG

```
cd downloads/harvester/mag
curl -O https://academicgraph.blob.core.windows.net/graph-2015-11-06/MicrosoftAcademicGraph.zip
7z x MicrosoftAcademicGraph.zip
```
