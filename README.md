[![CircleCI](https://circleci.com/gh/barone-dev/valid_thru.svg?style=svg)](https://circleci.com/gh/barone-dev/valid_thru)

# Valid Thru Service

---

All commands to execute this project can be found inside the Makefile. It's require python 3.6+

Step by step:

1 - Prepare your enviroment with:

$ **make prepare**

2 - This project uses Flask as a server for the application, to run this server use:

$ **make run_server**

The server runs on:

**http://localhost:8000**

The **available endpoints** are (the query params are just examples):

* **/valid-thru/?month=03&year=2028** *[GET]*
* **/client/** *[POST]*
* **/client/?id=3** *[GET, PUT, DELETE]*
