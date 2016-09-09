How to deploy

### Attention:current user is operation!
### You clone this repo into /home/operation/zhihu


* `cd ~` ,`virtualenv code`，`source ~/code/bin/activate` , to  create isolated Python environments

* `cd zhihu `，`pip install -r requirements.txt` , to install needed libraries 

* `supervisord -c supervisor.conf` ,run this project
