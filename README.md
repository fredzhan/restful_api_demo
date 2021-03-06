# Restful API Demo
## About
This is a simple demo of RESTful API based on `Python3` + `Flask` + `SqLite`. Data comes from comments for one [JD product page](https://item.jd.com/1384071.html) with the help of Python `requests` module.
## Quick start
**Env setup:**
1. Make sure you are using Linux environment with Python3 installed. And `python` command points to your Python3. Otherwise, for example if you are using `python3` command on your machine, replace `python` with it for all shell scripts in `./bin` folder.
2. Install all the packages needed by running:
`pip3 install -r Requirements.txt`

**2 components available:**
1. A spider crawling comments from jd.com. To launch:<br />
`cd restful_api_demo`<br />
`sh bin/run_spider.sh`<br />
Note:
    * By default, it crawls only first 6 pages. To change that please update value of `spider.request.dynamic_params.page` in `./config.yaml`
    * The comment ID is used as primary key. It follows 'insert or ignore' logic by checking if the primary key already exists. That means if you run with the same settings several times, it only inserts the new ones and ignore records that has been inserted earlier. You can find the summary info in log after each task.
    * By default, the log level is set as `info`, which already provides the needful info. To check out more details ( e.g. DB connection info and which specific records has been extraced ), just modify `system.logging_level` in `./config.yaml` to `debug`.
2. A RESTful API with GET method which allows searching for comment by keyword. To launch:<br />
`cd restful_api_demo`<br />
`sh bin/run_app.sh`<br />
Very soon the service will be up. The demo API has only 1 parameter, the search keyword. As an example, to retrieve all comments related to `物流` , use: `http://localhost:5000/api/v1/comments?kw=物流`
## Code structure
Though there are 2 components, code is mainly organized based on the RESTful API structure. The spider component is designed as one of the utils, i.e. data ingestion utility. With that, below is the intro for all important files and directories -

**./config.yaml**<br />
Configuration file with settings about DB, system and spider.

**./app.py**<br />
Main entry file for Flask.

**./bin/**<br />
A folder with components startup scripts.

**./models/**<br />
A folder with model classes which correspond to tables in DB. It also provides all table level CRUD methods to support API requests.

**./resources/**<br />
A folder containing pre-defined RESTFul resources, with all HTTP methods available to users.

**./utils/**<br />
A utility folder with helper classes and functions to be shared globally, e.g. DB, global variables and spider. 

**./logs/**<br />
A folder for logs.

**./Requirements.txt**<br />
Python package specifications for this project.
