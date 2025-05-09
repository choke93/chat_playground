readme

import warnings, requests
warnings.filterwarnings("ignore")
def disable_ssl_verification():
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    old_send = requests.Session.send

    def new_send(self, request, **kwargs):
        if 'openaipublic' not in request.url:
            kwargs['verify'] = False
        return old_send(self, request, **kwargs)

    requests.Session.send = new_send

disable_ssl_verification()
