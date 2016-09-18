# Intrinsic_Plagiarism_Analysis
This project is extended version of plagcomps/plagapp tool developed by Noah Carnahan & co (http://www.cs.carleton.edu/cs_comps/1314/dlibenno/final-results/plagcomps.pdf).
I have extended intrinsic plagiarism analysis module of this tool and updated with some new stylistic features and one additional outlier detection methods.
In the front end part, i have added some visualizations to make it more interactive to see the suspicious passages.
This extended tool is evaluated against vroniplag_medical test collections to measure the accuracy of stylistic features and created additional style models.The test collection contains all ground truths. Hence, it works as a framework to developers who are willing to test their new intrinsic plagiarism measures.

TO run the module the following packages are required to be installed. (Versions should as shown below)
Flask==0.10.1

Flask-WTF==0.9.4

Jinja2==2.7.1

MarkupSafe==0.18

PyBrain==0.3

PyYAML==3.10

SQLAlchemy==0.9.1

WTForms==1.0.5

Werkzeug==0.9.4

backports.ssl-match-hostname==3.4.0.2

gunicorn==18.0

itsdangerous==0.23

matplotlib==1.3.1

nltk==2.0.4

nose==1.3.0

numpy==1.8.0

psycopg2==2.5.2

pyparsing==2.0.1

python-dateutil==2.2

scikit-learn==0.14.1

scipy==0.13.2

six==1.5.2

tornado==3.2

wsgiref==0.1.2

Additionaly, database connectivity is required. The database used is postgresql.
The 'dbconstants.py' file in the 'plagcomps' folder must contain the database information as follows:

username='postgres'

password='12345678'

dbname='localhost:5432/postgres'


The username, password and the port number may differ from system to system. For those unfamiliar with postgresql, the
following link can serve as an introduction

https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-14-04
