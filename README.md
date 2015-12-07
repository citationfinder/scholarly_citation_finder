### Repositories

* [search-for-citations](https://sun01.pool.ifis.uni-luebeck.de/groppe/search-for-citations) Source code of the web service
    * [thesis](https://sun01.pool.ifis.uni-luebeck.de/rosenthal/search-for-citations-thesis) LaTex source files and cited papers of the thesis
    * [citations-deployment](https://sun01.pool.ifis.uni-luebeck.de/rosenthal/search-for-citations-deployment) Deployment scripts of the web serivce
    * [dataset](https://sun01.pool.ifis.uni-luebeck.de/rosenthal/search-for-citations-dataset) Data sets for testing 
* [publin](https://github.com/CiteEt/publin) Fork to integrate citation support
* ... further repos on [github.com/CiteET](https://github.com/CiteET)

### Setup

Install Python dependencies
	`pip install pyoai lxml subprocess32 requests beautifulsoup4`
	
```
Create folders:
 |- downloads
 |  |- harvester
 |     |- citeseerx
 |     |- dblp
 |
 |- lib
 |- log 
 ```