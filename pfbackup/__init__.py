"""Tool for creating pfSense firewall configuration backup

It can be used as an interactive tool from CLI or for unattended backups in 
containers, in which case, it is using following environment variables:

PF_URL: for storing web admin URL (e.g., https://192.168.1.1/)
PF_USER: username for making backups
PF_PASS: password for provided username
PF_CERT_VERIFY: set to False if self-signed certificate in use

When used in CLI, it will prompt for password if -p (--password) flag
not provided. Config will be printed to the stdout if -f (--file) omitted. 
"""

from pfbackup.pfsense import pfSense


__version__ = "1.1.1"
__all__ = ("pfSense")
