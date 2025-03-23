######## Alembic commands ##############

alembic init <foldername>
alembic revision -m "<Message>"
alembic upgrade <revisionnumber> ### this is taken from the file after running command 2

alembic revision --autogenerate -m "<message >" ## This will detect any change in models.py and automatically create the missing tables and columns, then run albemic upgrade
