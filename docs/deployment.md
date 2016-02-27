<h1>Deployment</h1>

## Ansible playbook

The Ansible Playbook can be used to deploy and setup SCF. The following components get installed and configured:

Server components

* Nginx, HTTP server
* Gunicorn, Python WSGI HTTP server
* Supervisor, Unix process control system
* Virtualenv, virtual python environment

Database

* PostgreSQL, Database management system

SCF

* Django, Python web framework
* Celery, task queue/job based
* RabbitMQ, message broker
* Grobid, PDF extractor

### Deploy webserver

Configure the script

* Copy the file `env_vars/development.yml.sample` to `env_vars/development.yml` and configure it (database password, etc.)
* Enter the IP of the server in in the `[webservers]` section of the `development` file

Run the complete playbook
```bash
ansible-playbook -i development site.yml --ask-become-pass
```

Run only the tasks marked with a `deploy` tag
```bash
ansible-playbook -i development site.yml --tags "deploy" --ask-become-pass
```

Alternatively use the Makefile
```bash
make install
make deploy
```

### Deploy Vagrant (virtual machine)

Configure the script

* Copy the file `env_vars/vagrant.yml.sample` to `env_vars/vagrant.yml` and configure it (database password, etc.)

Run Vagrant to download and setup a VirtualBox and then run the Ansible playbook
```bash
vagrant up
```

Open [http://192.168.33.15](http://192.168.33.15) or alternatively use `vagrant ssh` to connect to the machine. 

To re-run the Ansible playbook on the existing VM use
```bash
vagrant provision
```