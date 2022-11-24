import requests
import xmltodict

class Requests:

    def __init__(self, proxies = None, timeout = None):
        self._error= None
        self._proxies = proxies
        self._timeout = timeout

    @staticmethod
    def _xml_parser(xml):
        dict= xmltodict.parse(xml)['html']['body']['input']
        return dict

    @property
    def error(self):
        return self._error

    @staticmethod
    def _check_for_error(content):
        error= None
        try:
            if content['@name']=='ERROR':
                error= content['@value']
        except:
            pass

        return error

    def fetch(self, link, type):
        res= requests.get(link, verify=True, proxies=self._proxies, timeout=self._timeout)
        if not res.ok:
            self._error= res.text
            return False
        else:
            content= res.text
            if type=='xml':
                content= self._xml_parser(content)
                error= self._check_for_error(content)
                if error:
                    self._error= error
                    return False
                else:
                    return content
            else:
                return content
