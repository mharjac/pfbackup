import urllib.parse
import requests
import sys


class pfSense:
    def __init__(self, pf_url, pf_user, pf_pass, cert_verify = True):
        self.pf_url = pf_url
        self.pf_user = pf_user
        self.pf_pass = pf_pass
        self.cert_verify = cert_verify
        self.headers = {'Content-Type':'application/x-www-form-urlencoded'}
        self.response = ""

        self.client = requests.session()
        self._authenticate()

    def _get_csrf_token (self, csrf_length):
        csrf_token_offset = self.response.text.find("name=\'__csrf_magic\' value=") + 27
        return self.response.text[csrf_token_offset:csrf_token_offset + csrf_length]
    
    def _authenticate(self):
        self.response = self.client.get(self.pf_url, verify = self.cert_verify)
        csrf_token = self._get_csrf_token(110)
        payload = "__csrf_magic=" + urllib.parse.quote(csrf_token) + "&usernamefld=" + urllib.parse.quote(self.pf_user) + "&passwordfld=" + urllib.parse.quote(self.pf_pass) + "&login=Sign+In"
        self.response = self.client.post(self.pf_url, data = payload, headers = self.headers, verify = self.cert_verify)
        if self.response.text.find("Username or Password incorrect") != -1:
            sys.stderr.write(f"ERROR: Username or Password incorrect.\n")
            sys.exit(1)

    def get_config(self):
        csrf_token = self._get_csrf_token(55)
        payload = "download=download&donotbackuprrd=yes&__csrf_magic=" + urllib.parse.quote(csrf_token)
        self.response = self.client.post(self.pf_url + "/diag_backup.php", data = payload, headers = self.headers, verify = self.cert_verify)
        return self.response.text