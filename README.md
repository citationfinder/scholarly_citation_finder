### Repositories

* [search-for-citations](https://sun01.pool.ifis.uni-luebeck.de/groppe/search-for-citations) Source code of the web service
    * [thesis](https://sun01.pool.ifis.uni-luebeck.de/rosenthal/search-for-citations-thesis) LaTex source files and cited papers of the thesis
    * [deployment](https://sun01.pool.ifis.uni-luebeck.de/rosenthal/search-for-citations-deployment) Deployment scripts of the web serivce
    * [dataset](https://sun01.pool.ifis.uni-luebeck.de/rosenthal/search-for-citations-dataset) Data sets for testing 
* [publin](https://github.com/CiteEt/publin) Fork to integrate citation support
* ... further repos on [github.com/CiteET](https://github.com/CiteET)

### Setup

Create folders:
```
 |- downloads
 |  |- harvester
 |     |- citeseerx
 |     |- dblp
 |
 |- lib
 |- log 
```

#### Install dependencies

**For Ubuntu**

```
sudo apt-get install python python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev
```

Note: `libxml2-dev`, `libxslt1-dev`, `zlib1g-dev` are required for `lxml`

**Python dependencies**

```
pip install -r requirements.txt
```
 
 
### Code style
 
Style convention: [PEP 8](https://www.python.org/dev/peps/pep-0008/).

Tool: [pep8 ](https://pypi.python.org/pypi/pep8) with the param `--ignore=E265,E501,W293` (E265 _block comment should start with ‘# ‘_, E501 _line too long_, W293 _blank line contains whitespace_)
 