# genie
A RESTful test data management framework

## Assumptions
Basic understanding of git, aws, docker, python.

## Requirements
All the requirements listed below with asterisks are optional for actual production deployment of the genie framework but required for the *demo*.
 - Ubuntu 14.04 LTS *
 - Docker 17.03 *
 - git 1.9
 - nginx 1.4.6
 - gunicorn 19.7.1
 - Python 3.4
 - Eve 0.6.4
 - ELK stack (discussed below)

**Genie package dependencies**
```
Cerberus==0.9.2
Eve==0.6.4
Eve-SQLAlchemy==0.5.0
Events==0.2.2
Flask==0.10.1
Flask-PyMongo==0.5.1
Flask-SQLAlchemy==2.3.2
itsdangerous==0.24
Jinja2==2.10
MarkupSafe==0.23
pymongo==3.6.0
PyMySQL==0.8.0
simplejson==3.13.2
SQLAlchemy==1.2.2
Werkzeug==0.14.1
```


## Environment Setup
I am using AWS server to carry out the demo for this. I am launching `c3.xlarge (4 vCPU, 7.5 GiB, 2 x 40 SSD)` ec2 instance to have everything setup using a docker container. In production, it is good to have it installed in a swarm setup for continuity in case of server crash or for scaling & cluster management.

## Installation
I have used a user data for my ec2 instance which will install docker during the instance launch. If you have the server ready you can still use below as a shell script to install docker.

    #!/bin/bash
    set -e -x
    export DEBIAN_FRONTEND=noninteractive
    apt-get update && apt-get upgrade -y
    curl https://releases.rancher.com/install-docker/17.03.sh | sh
    echo "docker installed"
    usermod -aG docker ubuntu
    apt-get install tree

 - Install the latest version of docker-compose by ```sudo curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose```
 - Executable access to the user `sudo chmod +x /usr/local/bin/docker-compose`
 - Verify installation `docker-compose --version`
 - Verify installation `docker info`
 - I'm using an existing docker compose file to build ELK stack ([docker-elk by Anthony Lapenna](https://github.com/deviantony))
 - Clone docker elk to wherever you're interested. `https://github.com/deviantony/docker-elk.git`
 - To run ELK stack as containers, run the compose file using `docker-compose -f docker-compose-elk.yml up`
 - Build metricbeat
 - To run MySQL as containers, run `docker-compose -f docker-compose-mysql.yml up`
 - Install mysql `docker pull mysql:5.6`.
 - Running mysql in container `docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=password -d mysql:5.6` Default port exposed is 3306.
 - Install Python 3.6
```
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install python3.6
```
 - Install python virtualenv `sudo apt-get install python-virtualenv`
 - Install pip `sudo apt-get install python-pip python-dev build-essential`
 - Install nginx `sudo apt-get install nginx`
 - Build Genie
 - Build Apache JMeter

### AWS EC2 Security group
Following ports need to be open if it needs to be accessed from the internet or outside of the VPC.
|App/protocol|Port|Note|
|--|--|--|
|ssh|22||
|Genie|80|
|Elasticsearch|||
|Kibana|||
|MySQL|3306||
|adminer|8080|mysql admin work (optional)|


## Setup the genie/Eve dev-environment
We will setup a local development environment to carry out any sort of modifications or developments to our applications in future. (For this we will create a git repository)
### Setup python3.6 virtualenv
 - After python3.6, pip and virtualenv is installed. Run following command to create a virtual environment `virtualenv -p /usr/bin/python3.6 venv`. It will create a directory `venv` which will have all executables for the virtual environment.
 - Activate the virtual environment by running `source venv/bin/activate`. Now the environment is active and we can have our dependencies installed.

### Clone the repository
 - `git clone https://github.com/dnafication/genie.git`
 - cd into the project directory `cd genie`
 - Install the dependencies `pip install -r requirements.txt`
 - Ensure mysql service is running and is configured correctly in `settings.py`
 - Once the dependencies are successfully installed, we are ready to launch the dev version of application by simply running `python app.py`. It will start an http server which is running flask with eve and serving at port `5000`.
 - Open a browser and enter `http://<host>:5000` to access the app.

### Running MySQL in a compose file
We have an option to run it along with other containers using compose or as part of stack using a docker stack command. This will be discussed here in future.

 - Clone the repository `git clone https://github.com/dnafication/docker-elk.git`
 - Cd into the repo `cd docker-elk`
 - Assuming docker-compose is already installed, execute `docker-compose -f docker-compose-mysql.yml up`

### Post setup tree view (only directories)
The tree view of the local dev directory after the initial setup.

    .
    ├── docker-elk
    │   ├── elasticsearch
    │   │   └── config
    │   ├── extensions
    │   │   └── logspout
    │   ├── kibana
    │   │   └── config
    │   └── logstash
    │       ├── config
    │       └── pipeline



## Load data into genie using the client
I have built a client which can parse csv files and convert them to json object arrays to push into the application. This will be discussed in future.

## Deploy in nginx
 - ~~Build the docker image for genie `docker build -t genie .` This command uses the `Dockerfile` in the context.~~
 - ~~Run the image `docker run -p 80:80 genie`~~
 - Install gunicorn by running `pip install gunicorn` inside virtual environment.
 - Let flask figure out the settings file by setting the environment variable `EVE_SETTINGS` to the location of settings file. Example: `export EVE_SETTINGS=/path/to/settings.py` (this resides in the `genie` directory.
 - Run single worker gunicorn `gunicorn app.app:app` from working directory of `genie`
 - Run multiple workers `gunicorn --workers=4 app.app:app`
 - Ensure nginx  is installed.  Start nginx by `sudo /etc/init.d/nginx start`
 - Setup nginx as a reverse proxy to the gunicorn server running on localhost at port 8000 by using following config file
 - Create a server block in nginx by creating a file `/etc/nginx/sites-available/genie` with following content.
```
server {
	location / {
		proxy_pass http://127.0.0.1:8000;
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
	}
}
```
 - Create sym link to genie file in sites-enabled by executing `sudo ln -s /etc/nginx/sites-available/genie /etc/nginx/sites-enabled/genie`
 - Delete the default server block in sites-enabled directory `sudo rm /etc/nginx/sites-enabled/default`
 - Restart nginx `sudo /etc/init.d/nginx stop` then ` sudo /etc/init.d/nginx start`
 - The application is live.
 - Daemonize gunicorn `gunicorn --chdir /home/ubuntu/genie --daemon app.app:app`
 - Stop gunicorn
```
kill -9 `ps aux |grep gunicorn |grep genie | awk '{ print $2 }'`
```


## Warning/Disclaimer
I have overlooked many security aspects in order for it to work. Use this setup only for demo. To use this into production we need
 - Proper review of all the ports being open to the public.
 - Security testing (at least basic penetration testing)
 - MySQL root password is open in the compose file.
 - Settings file has MySQL password in plain text.