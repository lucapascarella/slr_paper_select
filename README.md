# Paper Selection App

This app is used to decide whether to include a paper in the systematic literature review. By default, each paper will be labeled by two people.  

It was developed to support the following paper:

Bin Lin, Nathan Cassee, Alexander Serebrenik, Gabriele Bavota, Nicole Novielli, Michele Lanza, *"Opinion Mining for Software Development: A Systematic Literature Review"*, 2021


## Setup

### Requirements

This application is developed with Python 3. To test the project, you can first create a virtual environment and then install the third party dependencies with the following commands in the root directory of the app:

```
$ python3 -m venv ./venv
$ source ./venv/bin/activate
(venv)$ pip3 install -r requirements.txt
```

Then you can set the ``FLASK_APP`` and ``FLASK_ENV`` environment variables to point to the application and enable the development mode:

```
(venv)$ export FLASK_APP=paper_select
(venv)$ export FLASK_ENV=development
```

### Initialize the database

To initialize the database, you can run the following command:

```
(venv)$ flask init-db
```

The schema of the database can be found in the file ``paper_select/schema.sql``. After the initialization, the database have no records. Thus, you need to dump your data into the database located in ``instance/paper_select.sqlite``.

We have provided a simple script (``dump_data.py``) and an example data file (``papers.csv``) in csv format for demonstration purpose. You can run ``python3 dump_data.py`` to insert the records into the database.    

### Run the application locally

To run the application locally, you can execute the following command:

```
(venv)$ flask run
```

By default, the application will be run on the port 5000. You can visit the application on ``http://127.0.0.1:5000``. 

## Deployment

To simplify the deployment, we have dockerized the application. That is, on a server supporting Docker, you can deploy the application by simply running the following command on the root directory of the project:

```
docker-compose up -d
```

The default host port is 5050, which can be changed in the ``docker-compose.yml`` file.
