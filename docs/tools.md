<h1>Development tools</h1>

## Django tips

Migrate a specific database or flush it
```bash
$ ./manage.py migrate --database=<database name>
$ ./manage.py flush --database=<database name>
```

Open Django shell for testing or debugging
```bash
$ python manage.py shell
>>> import django
>>> django.setup()
```


## PostgreSQL tips

Open PostgreSQL shell
```bash
$ psql -U <user_name> [<database_name>]
```

Create a user and a database
```sql
CREATE USER <user_name> WITH PASSWORD '<password>';
CREATE DATABASE <name> [OWNER <user_name>];
```


## RabbitMQ tips

Stop RabbitMQ
```bash
$ sudo -u rabbitmq rabbitmqctl stop
```