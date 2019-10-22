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

import datetime
import os
import getpass
import urllib3
import sys
import argparse
import pfbackup


def main():
    parser = argparse.ArgumentParser(prog="pfbackup")
    parser.add_argument("-U", "--url", help="pfSense web administration URL")
    parser.add_argument("-u", "--user", help="username for executing backup")
    parser.add_argument("-p", "--password", help="password for provided username; prompts if not provided")
    parser.add_argument("-f", "--filename", default="/dev/stdout", metavar="FILE", help="FILE to write backup; stdout if not provided")
    parser.add_argument("-n", "--no-verify", action="store_false", dest="verify", help="do not verify TLS certificate")
    parser.add_argument("-v", "--version", action="store_true", help="show version")
    options = parser.parse_args()

    time_stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    if options.version:
        print(pfbackup.__version__)
        sys.exit(0)
    elif options.url and options.user:
        username = options.user
        if options.password:
            password = options.password
        else:
            password = getpass.getpass("Input password: ")
        url = options.url
        cert_verify = options.verify
        filename = options.filename
    else:
        try:
            username = os.environ['PF_USER']
            password = os.environ['PF_PASS']
            url = os.environ['PF_URL']
            cert_verify = (True, False)[os.environ['PF_CERT_VERIFY'].upper() == "FALSE"]
            filename = f"config-{time_stamp}.xml"
        except KeyError as err:
            sys.stderr.write(f"ERROR: Missing {err} environment variable.\n")
            sys.exit(1)

    # To avoid "InsecureRequestWarning: Unverified HTTPS request is being made."
    # when self-signed certificate in use
    if cert_verify == False:
        urllib3.disable_warnings()

    pf = pfbackup.pfSense(url, username, password, cert_verify)
    config = pf.get_config()

    with open(filename, "w") as f:
        f.write(config)


if __name__ == "__main__":
    main()