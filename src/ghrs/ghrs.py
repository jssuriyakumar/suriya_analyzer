from base64 import b64encode, b64decode
from os import environ, makedirs, path
from tqdm import tqdm
import requests
from .query import Query


class GHRS(Query):
    """
    Class for initializing a GHRS connection.
    """

    api_url = ("https://hcms.saipemnet.saipem.intranet/psc/GHRS_3/EMPLOYEE"
               "/PSFT_HR/q/?ICAction=ICQryNameURL="
               "PUBLIC.SA_REPORT_TS_XSIGHT_ITA")

    auth_url = 'https://wam.saipem.com'

    header = {
        'Host': 'hcms.saipemnet.saipem.intranet',
        'Accept-Encoding': 'gzip, deflate, br',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google \
            Chrome";v="90"',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'Origin': 'https://hcms.saipemnet.saipem.intranet',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': api_url,
        'Accept-Language': 'en'}

    def authenticate(self, cert=''):
        """
        This method authenticates the session
        when the status code = 200.

        Upon initialization, when the status of the session
        code matches 200, it authenticates the session.

        Args:
            USER (str):
                      base64 Decrypted User id is accessed from the
                      __init__ method.

            PASS (str):
                      base64 Decrypted Password is accessed from the
                      __init__ method.

        Returns:
            list: A session with status code 200 is established.
        """

        self.session = requests.Session()
        self.session.verify = True
        if cert:
            self.session.verify = cert
        responses = []
        responses.append(self.session.get(self.api_url,
                         allow_redirects=False))
        for i in tqdm(range(0, 25, 1)):
            if responses[-1].status_code == 302:
                if responses[-1].next.url[:len(self.auth_url)] == \
                        self.auth_url:
                    responses[-1].next.prepare_auth((self.USER,
                                                     self.PASS))
                responses.append(self.session.send(responses[-1].next,
                                 allow_redirects=False))
            else:
                break
        return responses[-1]

    def store_credentials(self, location):
        """
        This method requires the user to enter the UserId and Password for
        creating user credentials, if not available.

        Args:
            Location (str): C:\\Python\\vault\\cred.dat Path to  cred.dat,
            containing the user credentials.

        Returns:
               This method stores the user credentials
               and saves it in C:\\Python\\vault\\cred.dat as base64
               encrypted file.
        """

        print('The Credentials supplied will be stored in an encrypted'
              ' format in your computer\n\n')
        self.USER = input('Enter your AlphaNumeric User ID\n')
        self.PASS = input('\nEnter your Password\n')
        with open(location, 'wb') as f:
            f.write(b64encode(bytes(f'{self.USER}:{self.PASS}',
                                    'utf-8')))

    def __init__(self, *args, **kwargs):
        """
        Constructor Method for Class GHRS used to initializing an object.

        Upon initialization, this method checks for existence of user
        credentials in your local system. If not available, it creates
        a directory in path C:\\Python\\vault.This method also acknowledges
        the Session authentication.

        This method redirects to store_credentials method where the user
        credentials are encrypted and stored in the directory.


        Args:
            vault (str): C:\\Python\\vault Path to the directory where the
             user credentials has to be stored.

            credentials (str): C:\\Python\\vault\\cred.dat Path to  cred.dat,
             containing the user credentials.

        Returns:
                This method initializes the user credentials by creating
                new credentials or decrypting the credentials, based on need
                and acknowledges the session authentication.
        """
        vault = path.join(environ['systemdrive'] + '\\', 'Python', 'vault')
        credentials = path.join(vault, 'cred.dat')
        certificate = ''
        if 'cert' in kwargs:
            if path.exists(kwargs['cert']):
                certificate = kwargs['cert']
        if path.exists(vault):
            if path.exists(credentials):
                with open(credentials, 'rb') as f:
                    self.USER, self.PASS = b64decode(
                        f.read()).decode('utf-8').split(':')
            else:
                self.store_credentials(credentials)
        else:
            makedirs(vault)
            self.store_credentials(credentials)
        self.response = self.authenticate(cert = certificate)
        if self.response.status_code == 200:
            print('Session Authenticated!')
        else:
            print('Session Authentication Failed!\n'
                  'Recheck your Credentials and Network')
