import requests 
import xmltodict

class Requests:

    def __init__(self):
        self._error= None 

    def _xml_parser(self, xml):
        dict= xmltodict.parse(xml)['html']['body']['input']
        return dict

    @property
    def error(self):
        return self._error

    def _check_for_error(self, content):
        error= None
        try: 
            if content['@name']=='ERROR':
                error= content['@value']
        except:
            pass 
        
        return error

    def fetch(self, link, type):
        res= requests.get(link, verify=True)
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
