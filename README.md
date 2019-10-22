# pfBackup

## Summary

Simple utility for backing up pfSense configuration which uses web admin interface.

## Installation
### Create backup user account
It is recommended to create a dedicated user account with limited permissions for backup purposes. This user should have "WebCfg - Diagnostics: Backup & Restore" permission. Please check [pfSense documentation](https://docs.netgate.com/pfsense/en/latest/usermanager/index.html) if you are not sure how to do this. 

### Installation form PyPI:
```
pip3 install pfbackup
```
### Docker
You can download the image from Docker Hub:
```
docker pull mharjac/pfbackup
```
Or build it on your own:
```
docker build -t pfbackup https://github.com/mharjac/pfbackup.git#:docker
```
Create a volume for storing backups:
```
docker volume create pfbackup-firewall-1
```
Create a container:
```
docker run -d --name=pfbackup-firewall-1 -e PF_URL="https://192.168.1.1" -e PF_USER="backusr" -e PF_PASS="somesuperstrongpassword" -e PF_CERT_VERIFY="true" --mount=src=pfbackup-firewall-1,dst=/backup pfbackup:latest
```
And finally, for unattended regular backups, create a cron job which will execute:
```
docker start pfbackup-firewall-1
```
### Install from Snap Store
```
snap install pfbackup
```
## Usage
It can be used as an interactive tool from CLI:
```
pfbackup -U https://192.168.1.1 -u user1 -p passw0rd -f ./backup.xml
```
When used in CLI, it will prompt for password if -p (--password) flag is not provided. Also, without -f (--file) flag, config will be printed to the stdout.  

It can also be used for unattended backups (e.g., in containers), in which case, it requires following environment variables:  
* PF_URL: for storing web admin URL (e.g., https://192.168.1.1/)
* PF_USER: username for making backups
* PF_PASS: password for provided username
* PF_CERT_VERIFY: set to False if self-signed certificate in use  
```
export PF_URL="https://192.168.1.1" PF_USER="user1" PF_PASS="passw0rd" PF_CERT_VERIFY="True"
pfbackup
```
When executed in unattended mode, configuration backup will be saved in execution directory as `config-{time_stamp}.xml`.
