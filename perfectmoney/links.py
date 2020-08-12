class LinksBase:

    def __init__(self, account_id, password):
        self._account_id= account_id
        self._password= password
        self._base_url= 'https://perfectmoney.is/acct/'

    def _add_parameter(self,link, parameter_dic, xml_type= True, auth=True):
        if auth:
            link= self._get_auth_link(link)
        for parameter, value in parameter_dic.items():
            if not value:
                continue

            parameter= parameter.replace(' ','')
            value= str(value).replace(' ','')

            link= link+'&'+parameter+'='+value
        
        if xml_type:
            link= link+'&api_version=1'
        
        return link
        
    def _get_auth_link(self, link):
        auth_link= link+'AccountID='+self._account_id+'&PassPhrase='+self._password 
        return auth_link

class Links(LinksBase):

    def get_balance_link(self):
        parameters= {}
        balance_base= self._base_url+'balance.asp?'
        return self._add_parameter(balance_base, parameters)

    def get_confirm_link(self, 
        payer_account, 
        payee_account, 
        amount, 
        memo, 
        payment_id,
        code,
        period
        ):

        parameters= {
            'Payer_Account': payer_account,
            'Payee_Account': payee_account,
            'Amount': amount,
            'Memo': memo,
            'PAYMENT_ID': payment_id,
            'code': code,
            'period': period
        }
        confirm_base= self._base_url+'confirm.asp?'        
        return self._add_parameter(confirm_base, parameters)

    def get_verify_link(self,
        payer_account, 
        payee_account, 
        amount, 
        memo, 
        payment_id,
        code,
        period    
        ):

        parameters= {
            'Payer_Account': payer_account,
            'Payee_Account': payee_account,
            'Amount': amount,
            'Memo': memo,
            'PAYMENT_ID': payment_id,
            'code': code,
            'period': period
        }        

        verify_base= self._base_url+'verify.asp?'        
        return self._add_parameter(verify_base, parameters)

    def get_protection_link(self,
        batch, 
        code, 
        ):

        parameters= {
            'batch ': batch ,
            'code': code,
        }        

        protection_base= self._base_url+'protection.asp?'        
        return self._add_parameter(protection_base, parameters)

    def get_account_name_link(self,
        account
        ):

        parameters= {
            'Account': account ,
        }      

        acc_name_base= self._base_url+'acc_name.asp?'        
        return self._add_parameter(acc_name_base, parameters)        

    def get_history_link(self,
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
        ):

        parameters= {
            'startmonth ': startmonth, 'startday':startday, 'startyear':startyear,
            'endmonth': endmonth, 'endday': endday, 'endyear': endyear, 
            'paymentsmade': paymentsmade,
            'paymentsreceived': paymentsreceived,
            'batchfilter': batchfilter,
            'counterfilter': counterfilter,
            'metalfilter': metalfilter,
            'desc': desc,
            'oldsort': oldsort,
            'payment_id': payment_id
        }       

        historycsv_base= self._base_url+'historycsv.asp?'        
        return self._add_parameter(historycsv_base, parameters)

    def get_rates_link(self, currency):
        parameters= {
            'CUR': currency
        }

        rates_base= self._base_url+'rates.asp?'        
        return self._add_parameter(rates_base, parameters, auth=False)

    def get_voucher_list_links(self, 
        startmonth, startday, startyear,
        endmonth, endday, endyear,    
        ev_number,
        batchfilter,
        counterfilter,
        currency,
        desc,
        oldsort
        ):

        parameters= {
            'startmonth ': startmonth, 'startday':startday, 'startyear':startyear,
            'endmonth': endmonth, 'endday': endday, 'endyear': endyear, 
            'ev_number': ev_number,
            'batchfilter': batchfilter,
            'counterfilter': counterfilter,
            'currency': currency,
            'desc': desc,
            'oldsort': oldsort,
        }

        voucher_base= self._base_url+'evcsv.asp?'        
        return self._add_parameter(voucher_base, parameters)

    def get_voucher_create_links(self, payer_account, amount):
        parameters= {
            'Payer_Account': payer_account,
            'Amount': amount
        }
        base= self._base_url+'ev_create.asp?'        
        return self._add_parameter(base, parameters)

    def get_voucher_return_links(self, ev_number):
        parameters= {
            'ev_number': ev_number,
        }
        base= self._base_url+'ev_remove.asp?'        
        return self._add_parameter(base, parameters)

    def get_voucher_activation_links(self, payee_account, ev_number, ev_code):
        parameters= {
            'Payee_Account': payee_account,
            'ev_number': ev_number,
            'ev_code': ev_code
        }
        base= self._base_url+'ev_activate.asp?'        
        return self._add_parameter(base, parameters)
