
# **Project_CFG_team3** ![](../../../Desktop/footer.png)
________
A group project undertaken as a part of the CFG Software stream


## **About** 
 _____

**Sherfood** is a food sharing web application. We decided to build this application because tons of food is thrown away all over the world daily.

This is harmful, not only for moral reasons, but also drains our pockets.
In a situation where we buy too much food than it was necessary, it is better to share the excess food than to throw it away.

Our app helps to contact people who have food to share with those who are looking for it. Sherfood idea is in line with the idea of freeganism and less waste.

## Our team 💃💃💃💃
____
* [Urszula Kamińska](https://github.com/urszkam)

* [Keziah Belinda Malungu](https://github.com/KBelMal)

* [Darya Staliarova](https://github.com/daryaordaria)

* [Aleksandra Grunt-Mejer](https://github.com/kokoszoszana)

## Installation 
______

1. Clone the repository

```$ git clone git@github.com:daryaordaria/Project_CFG_team3.git```

2. Change the directory to Project_CFG_team3 on your local machine:


```$ cd Project_CFG_team3```

## Requirements
______
* blinker==1.5
* certifi==2022.9.24
* charset-normalizer==2.1.1
* click==8.1.3
* Flask==2.2.2
* Flask-Mail==0.9.1
* Flask-MySQLdb==1.0.1
* haversine==2.7.0
* idna==3.4
* importlib-metadata==5.0.0
* itsdangerous==2.1.2
* Jinja2==3.1.2
* MarkupSafe==2.1.1
* mysql-connector==2.2.9
* mysqlclient==2.1.1
* requests==2.28.1
* urllib3==1.26.12
* Werkzeug==2.2.2
* zipp==3.10.0

To install these requirements, run in the terminal :


```$ pip install -r requirements.txt```

## Configuration 
_________

1. Set up 'Sherfood' database

Run ```db.sql``` script in  MySQL workbench to set up the database

2. Configure Database 

Open config.py, replace ```HOST```, ```USER```, ```PASSWORD``` with your own data:

```HOST="Your DB Host name"```

```USER="Your user name"```

```PASSWORD = "Your DB password"```

```EMAIL_USER = "Company email address"```

```EMAIL_PASSWORD ="App password"```

To generate ```EMAIL_PASSWORD```, user has to set up 2-step verification on the account so that they could have access to the generation of a 16-digit app password.

This kind of password is usually used for less secure apps or if you don't want to share your password with a particular application.

```For gmail```, please follow this instruction: https://support.google.com/mail/answer/185833?hl=en-GB



3. Configure API 

Please register on https://console.cloud.google.com/ for an api key to allow the usage of geolocalisation accessible
via def extract_lat_long_via_address() and calculate_distance(). This will allow you to see closest annoucements.

When you generate your api key please insert it into string below.

```Example api key = AIzaSyApyx4KbXuO-hBRceBu3LugFm-rYdAlvWR``` (This one IS NOT working)

```GOOGLE_API_KEY = f"AIzaSyApyx4KbXuO-hBRceBu3LugFm-rYdAlvWR"```


## How to run the project 
________

Make sure you are in the Project_CFG_team3 directory and run the following command :


For **Mac** and **Linux** users:

```export FLASK_APP=Project_CFG_team3```

```export FLASK_DEBUG=1```

```flask run```

For **Windows** users:

```$env:FLASK_APP="Project_CFG_team3"```

```python -m flask run```
