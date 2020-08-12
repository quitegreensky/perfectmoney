from .links import Links
from .requests import Requests
from .utils import csv_to_list, rates_to_dic

class PerfectMoney(Links):
    
    def __init__(self, account_id, password):
        super().__init__(account_id, password)
        self.req= Requests()
        self._error= None 
        self._address_prefix= {
            'U': 'USD',
            'E': 'EUR',
            'G': 'GOLD',
            'B': 'BTC'
        }

    def __call__(self):
        self._error= None 

    @property
    def error(self):
        return self._error
        
    def balance(self):
        balance_dic= {
            'USD': [],
            'EUR': [],
            'GOLD': [],
            'BTC': []
        }
        link= self.get_balance_link()
        content= self.req.fetch(link, type='xml')

        if not content:
            self._error= self.req.error
            return False
        else:
            for address in content:
                asset= self._address_prefix[address['@name'][0]]
                balance_dic[asset].append({
                    address['@name']: address['@value']
                })

            return balance_dic

    def spend(self, payer_account, payee_account, amount, memo= '', payment_id= '', code= '', period= None):
        '''
        AccountID	:Perfect Money® account login  (payer)	-> 10000
        PassPhrase	:Perfect Money® account password -> This1isnotReal
        Payer_Account	:Your Perfect Money® account to spend from	-> U1234567
        Payee_Account	:Perfect Money® account to spend to	-> U7654321
        Amount	:Amount to be spent. Must be positive numerical amount.	-> 19.95
        Memo	:Up to 100 characters to be placed in memo section of transaction. The memo is visible to both payer and payee.	-> Thanks for dinner.
        PAYMENT_ID	:Optional merchant reference number. If present, this string of up to 50 characters is placed in the transaction. Payer and/or payee may search/query account history for this value.	-> ID-322223
        code 	:(Optional) Pass this value if only you want to use transfer protection code. If protection code is present, payee must enter this code to get money to his/her account.
                Must be alpha-numerical string of length from 1 to 20 chars. ->	mycode123
        Period	:(Optional) You need to pass this value if only you want to use transfer protection code.
                Number of days you want your transfer with protection code to be valid. If payee does not enter protection code during this period, money will be transferred back to your account.
                Must be integer value from 1 to 365 days. ->	3
        '''        
        
        link= self.get_confirm_link(payer_account, payee_account, amount, memo, payment_id, code, period) 
        content= self.req.fetch(link, type='xml')
        if not content:
            self._error= self.req.error
            return False
        else:
            dic= {}
            for items in content:
                dic[items['@name']]= items['@value']
            return dic 

    def verification(self, payer_account, payee_account, amount, memo= '', payment_id= '', code= '', period= None):

        link= self.get_verify_link(payer_account, payee_account, amount, memo, payment_id,code,period)
        content= self.req.fetch(link, type='xml')
        if not content:
            self._error= self.req.error
            return False
        else:
            dic= {}
            for items in content:
                dic[items['@name']]= items['@value']
            return dic 

        return dic 

    def protection_code_confirmation(self, batch, code):
        link= self.get_protection_link(batch, code)
        content= self.req.fetch(link, type='xml')
        if not content:
            self._error= self.req.error
            return False
        else:
            dic= {}
            for items in content:
                dic[items['@name']]= items['@value']
            return dic 

    def account_name_fetch(self, account):
        link= self.get_account_name_link(account)
        content= self.req.fetch(link, type='plain')
        if not content:
            self._error= self.req.error
            return False

        if 'ERROR:' in content:
            self._error= content
            return False 
        else:
            return content

    def history(self,
        startmonth='', startday='', startyear='',
        endmonth='', endday='', endyear='',
        paymentsmade='', 
        paymentsreceived='',
        batchfilter='',
        counterfilter='',
        metalfilter='',
        desc='',
        oldsort='',
        payment_id=''    
        ):

        link= self.get_history_link(
        startmonth, startday, startyear,
        endmonth, endday, endyear,
        paymentsmade, 
        paymentsreceived,
        batchfilter,
        counterfilter,
        metalfilter,
        desc,
        oldsort,
        payment_id            
        )
        content= self.req.fetch(link, type='plain')
        if not content:
            self._error= self.req.error
            return False

        if 'Error:' in content:
            self._error= content
            return False 
        else:
            content= csv_to_list(content)
            return content        

    def rates(self, currency='USD'):
        link= self.get_rates_link(currency)
        content= self.req.fetch(link, type='plain')
        if not content:
            self._error= self.req.error
            return False
        else:
            content= rates_to_dic(currency, content)
            return content

    def voucher_list(self, 
        startmonth='', startday='', startyear='',
        endmonth='', endday='', endyear='',    
        ev_number='',
        batchfilter='',
        counterfilter='',
        currency='',
        desc='',
        oldsort=''    
        ):

        link= self.get_voucher_list_links(
            startmonth, startday, startyear,
            endmonth, endday, endyear,    
            ev_number,
            batchfilter,
            counterfilter,
            currency,
            desc,
            oldsort
            )

        content= self.req.fetch(link, type='plain')
        if not content:
            self._error= self.req.error
            return False
        else:
            content= csv_to_list(content)
            return content        

    def voucher_create(self, payer_account, amount):
        link= self.get_voucher_create_links(payer_account, amount)
        content= self.req.fetch(link, type='xml')
        if not content:
            self._error= self.req.error
            return False
        else:
            dic= {}
            for items in content:
                dic[items['@name']]= items['@value']
            return dic         

    def voucher_return(self, ev_number):
        link= self.get_voucher_return_links(ev_number)
        content= self.req.fetch(link, type='xml')
        if not content:
            self._error= self.req.error
            return False
        else:
            dic= {}
            for items in content:
                dic[items['@name']]= items['@value']
            return dic                     

    def voucher_activation(self, payee_account, ev_number, ev_code):
        link= self.get_voucher_activation_links( payee_account, ev_number, ev_code)
        content= self.req.fetch(link, type='xml')
        if not content:
            self._error= self.req.error
            return False
        else:
            dic= {}
            for items in content:
                dic[items['@name']]= items['@value']
            return dic                