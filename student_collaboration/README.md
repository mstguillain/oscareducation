How to install this module for existing users ?

python manage.py runscript StudentCollaboratorCreator

Run the tests

python manage.py test student_collaboration

Run this command to add all defined jobs from CRONJOBS to crontab (of the user which you are running this command with):

python manage.py crontab add

show current active jobs of this project:

python manage.py crontab show

removing all defined jobs is straight forward:

python manage.py crontab remove