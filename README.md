Online Banking System
A Django based Open source Advance Banking project with complete account management, loan management, transactions history, etc

Features:
1)User Authentication and Authorization 
2)Account Management, Transactions and its History, Loan Management
3)Online Banking Security : Two-factor authentication, Tracked suspicious login attempt and force
blocking, Email Verification, Implemented session management, Notifications and Alerts
Send email  for transactions, account updates.
4)Admin Dashboard, Customer Support and  Reports Generation 

Package                Version
---------------------- ----------
asgiref                3.7.2
certifi                2023.11.17
cffi                   1.16.0
charset-normalizer     3.3.2
cryptography           42.0.2
defusedxml             0.7.1
Django                 5.0.1
django-axes            6.3.0
django-ipware          6.0.3
idna                   3.6
mysql-connector-python 8.2.0
mysqlclient            2.2.1
oauthlib               3.2.2
pillow                 10.2.0
pip                    23.3.2
protobuf               4.21.12
pycparser              2.21
pycryptodome           3.20.0
PyJWT                  2.8.0
python-ipware          2.0.1
python3-openid         3.2.0
requests               2.31.0
requests-oauthlib      1.3.1
setuptools             69.0.3
sqlparse               0.4.4
tzdata                 2023.4
urllib3                2.1.0
wheel                  0.42.0


Authentication: Custom Authentication

Database: MySql

To Run Project:
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

TO CREATE SUPERUSER:
python manage.py createsuperuser
