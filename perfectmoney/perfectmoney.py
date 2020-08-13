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
        Payer_Account:	Your Perfect Money® account to spend from	-> U1234567
        Payee_Account:	Perfect Money® account to spend to	-> U7654321
        Amount:	Amount to be spent. Must be positive numerical amount.	-> 19.95
        Memo:	Up to 100 characters to be placed in memo section of transaction. The memo is visible to both payer and payee.	-> Thanks for dinner.
        PAYMENT_ID:	Optional merchant reference number. If present, this string of up to 50 characters is placed in the transaction. Payer and/or payee may search/query account history for this value.	-> ID-322223
        code:	(Optional) Pass this value if only you want to use transfer protection code. If protection code is present, payee must enter this code to get money to his/her account.
                Must be alpha-numerical string of length from 1 to 20 chars. ->	mycode123
        Period: (Optional) You need to pass this value if only you want to use transfer protection code.
                Number of days you want your transfer with protection code to be valid. If payee does not enter protection code during this period, money will be transferred back to your account.
                Must be integer value from 1 to 365 days. ->	3
        
        #==========
        # Output
        #==========
        ERROR	Spend did not occur if this field present. Text description of error.	Invalid PassPhrase.
        Payee_Account_Name	Name of account of payee. Actually the text payee entered in his/her “Account name” profile field.	John’s shop
        Payer_Account	Perfect Money® account of sender.	U1234567
        Payee_Account	Perfect Money® account of recipient of spend.	U7654321
        PAYMENT_AMOUNT	Numerical amount of spend as entered. This is the same value as the Amount input field.	5.15
        PAYMENT_BATCH_NUM	PerfectMoney batch number generated for this transaction. Payer and/or payee may query/search account history by this number.	758094
        PAYMENT_ID	Optional merchant reference number. If present on input, this string of up to 50 characters is returned on output. Payer and/or payee may search/query account history for this value.	ID-322223
        code 	(Optional) This value is present only for transfers with protection code. If protection code is present, payee must enter this code to get money to his/her account.
        Can  be alpha-numerical string of length from 1 to 20 chars.	mycode123
        Period	(Optional) This value is present only for transfers with protection code. Number of days you want your transfer with protection code to be valid. If payee does not enter protection code during this period, money will be transferred back to your account.
        Must be integer value from 1 to 365 days.	3
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
        '''
        Payer_Account	Perfect Money® account of sender.	U1234567
        Payee_Account	Perfect Money® account to spend to	U7654321
        Amount	Amount to be spent. Must be positive numerical amount..	19.95
        Memo	Up to 100 characters to be placed in memo section of payment. The memo is visible to both payer and payee.	Thanks for dinner.
        PAYMENT_ID	Optional merchant reference number. If present on input, this string of up to 50 characters is returned on output. Payer and/or payee may search/query account history for this value.	ID-322223
        code 	(Optional) Pass this value if only you want to use transfer protection code. If protection code is present, payee must enter this code to get money to his/her account.
            Must  be alpha-numerical string of length from 1 to 20 chars.	mycode123
        period	(Optional) You need to pass this value if only you want to use transfer protection code.
            Number of days you want your transfer with protection code to be valid. If payee does not enter protection code during this period, money will be transferred back to your account.
            Must be integer value from 1 to 365 days.	3

        #==========
        # Output
        #==========
        ERROR	Verification is unsuccessful and did not occur if this field present. Text description of error.	Invalid PassPhrase.
        Payee_Account_Name	Name of account of payee. Actually the text payee entered in his/her “Account name” profile field.	John’s shop
        Payer_Account	Perfect Money® account of sender.	U1234567
        Payee_Account	Perfect Money® account of recipient of spend.	U7654321
        PAYMENT_AMOUNT	Numerical amount of spend as entered. This is the same value as the Amount input field.	5.15
        PAYMENT_ID	Optional merchant reference number. If present on input, this string of up to 50 characters is returned on output. Payer and/or payee may search/query account history for this value.	ID-322223
        code 	(Optional) This value is present only for transfers with protection code. If protection code is present, payee must enter this code to get money to his/her account.
            Can  be alpha-numerical string of length from 1 to 20 chars.	mycode123
            period	(Optional) This value is present only for transfers with protection code. Number of days you want your transfer with protection code to be valid. If payee does not enter protection code during this period, money will be transferred back to your account.
            Must be integer value from 1 to 365 days.	3
        '''
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
        '''
        batch 	Perfect Money® batch number of transaction you want to confirm with protection code.
            Must  be numerical value.	758094
        code 	Perfect Money® protection code entered by payer of this transaction.
            Can  be alpha-numerical string of length from 1 to 20 chars.	somecode321
        #==========
        # Output
        #==========
        ERROR	Confirmation  is unsuccessful and did not occur if this field present. Text description of error.	Invalid PassPhrase.
        PAYMENT_BATCH_NUM	Perfect Money® batch number of transaction you just confirmed (enrolled) with protection code.
        Numerical value.	758094
        code 	Perfect Money® protection code entered by payer of this transaction.
            Can  be alpha-numerical string of length from 1 to 20 chars.	somecode321
        '''        
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
        '''
        Account	Perfect Money® account ID	U1234567
        #==========
        # Output
        #==========
        Account name fetching cannot be completed if ERROR prefix present followed by text description of error.	ERROR: Invalid PassPhrase.
        Account name field of Account owner.	John’s shop
        '''        
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
        '''
        startmonth,startday,startyear   These three fields define the starting day to gather account history from. Month should be a number from 1 to 12, day should be a number from 1 to 31 and year should be a 4 digit number from 2007 onward.
        endmonth, endday, endyear	These three fields define the ending day to gather account history from. Month should be a number from 1 to 12, day should be a number from 1 to 31 and year should be a 4 digit number from 2007 onward.
            History will be provided for records from the beginning of the start date fields to the end of the end date fields. For instance, the example values would retrieve one complete month of data for the month of December 2007.
        paymentsmade	If present on input, Perfect Money® payments made are included in the history display. To not include Perfect Money® payments made, do not include this as an input field.
        paymentsreceived	If present on input, Perfect Money® payments received are included in the history display. To not include Perfect Money® payments received, do not include this as an input field.
        batchfilter	If present on input, only transactions that have this value as a batch number are displayed.
        counterfilter	If present on input, only transactions that have this PerfectMoney account number as a counter part (payments to/from this account number) are displayed.
        metalfilter	If present on input, only transactions that use the given currency units are displayed. Legal values are 1, 2 and 3 corresponding to US Dollars, Euro, and Gold troy oz.
        desc	If present, sort records in descending order instead of the default ascending order.
        oldsort	If present, defines the column to sort the history transactions on. (Default is timestamp). Choices are tstamp, batch_num, metal_name, counteraccount_id and amount corresponding to the available columns returned.
        payment_id	If present on input, only transactions that have this value as a payment_id are displayed.

        #==========
        # Output
        #==========
        Batch	The batch number of the transaction	1289
        Time	Time of transaction in GMT.	09/08/2000 00:03
        Type	Transaction Type. Possible values are: Charge, Income
        Currency	Name of Perfect Money®  currency transaction occurred in. Possible values are: USD, EUR , Troy oz. (GOLD), BTC (Bitcoin)	USD
        Amount	The actual numerical value of transaction.	19.95
        Fee	The amount of fee of the given transaction.	0.12
        Payer Account	PerfectMoney payer account ID.	U1234567
        Payee Account	PerfectMoney payee account ID.	U7654321
        Payment ID	The value optionally provided by merchant through PerfectMoney SCI or API interface.	ID-123
        Memo	Memo corresponding to this transaction.	Income 19.95 USD from account U1234567.  
        '''

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

    def rates(self, cur='USD'):
        '''
        CUR	Optional input field indicating display of exchange rates in this currency. Default is US Dollars. Choices are: USD = US Dollars EUR = Euro GOLD = Gold ounces (toy) BTC = Bitcoin

        '''        
        link= self.get_rates_link(cur)
        content= self.req.fetch(link, type='plain')
        if not content:
            self._error= self.req.error
            return False
        else:
            content= rates_to_dic(cur, content)
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
        '''
        startmonth, startday, startyear	These three fields define the starting day to gather e-voucher listing from. Month should be a number from 1 to 12, day should be a number from 1 to 31 and year should be a 4 digit number from 2007 onward.
        Please note this date means the date when e-voucher was created.
        endmonth, endday, endyear	These three fields define the ending day to gather e-voucher listing from. Month should be a number from 1 to 12, day should be a number from 1 to 31 and year should be a 4 digit number from 2007 onward.
            Listing will be provided for e-vouchers from the beginning of the start date fields to the end of the end date fields. For instance, the example values would retrieve one complete month of data for the month of December 2007.
        ev_number	If present on input, only Perfect Money® e-Voucher with that number is included in the listing  display.	0123456789
        batchfilter	If present on input, only e-Voucher that have this value as a batch number is displayed.	1289
        counterfilter	If present on input, only e-Vouchers that have this PerfectMoney account as a counter part (payments to/from this account number) are displayed.	U1234567
        currency	If present on input, only e-Vouchers that use the given currency units are displayed. Legal values are 1, 2 and 3 corresponding to US Dollars, Euro, and Gold troy oz.	1
        desc	If present, sort records in descending order instead of the default ascending order.	1
        oldsort	If present, defines the column to sort the e-Vouvher listing  on. (Default is created). Choices are created, amount, currency and batch corresponding to the available columns returned.	amount

        #==========
        # Output
        #==========
        Created	Time of e-Voucher creation in GMT.	09/08/2000 00:03
        e-Voucher number	The number of the e-Voucher (contains 10 digits)	0123456789
        Activation code	The activation code of the e-Voucher (contains 16 digits)	0123456789012345
        Currency	Name of Perfect Money®  e-Voucher c occurred in. Possible values are: USD EUR Troy oz. (GOLD) BTC (Bitcoin)	
        Batch	The batch number of the e-Voucher creation transaction	1289
        Payer Account	PerfectMoney payer account ID (e-Voucher creator).	U1234567
        Payee Account	PerfectMoney payee account ID (e-Voucher activator).  If e-Voucher is not activated – empty value.	U7654321
        Activated	Time of e-Voucher activation in GMT. If e-Voucher is not activated – empty value.	09/08/2000 00:03
        Amount	The actual nominal value of e-Voucher.	19.95

        '''

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
        '''
        Payer_Account	Your Perfect Money® account to spend from	U1234567
        Amount	Amount to be spent. Must be positive numerical amount.
            As a result e-Voucher of this nominal will be created.	19.95
        #==========
        # Output
        #==========
        ERROR	e-Voucher was not created if this field present. Text description of error.	Invalid PassPhrase.
        Payer_Account	Perfect Money® account of e-Voucher buyer.	U1234567
        PAYMENT_AMOUNT	Numerical amount of spend as entered. This is the total amount you payed icluding fee.	20.05
        PAYMENT_BATCH_NUM	PerfectMoney batch number generated for this transaction. You may query/search account history by this number.	758094
        VOUCHER_NUM	Unique number of purchased e-Voucher contaning 10 digits.	01234567891
        VOUCHER_CODE	Activation code of purchased e-Voucher contaning 16 digits.	0123456789123456
        VOUCHER_AMOUNT	Nominal amount of e-Voucher. This is the same value as the Amount input field.	19.95

        '''
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
        '''
        ev_number	Your Perfect Money® e-Voucher unique number you want to return.
            In case of success you will get e-Voucher nominal amount back to account you used to create this e-Voucher.	01234567891

        #==========
        # Output
        #==========
        ERROR	e-Voucher was not returned if this field present. Text description of error.	Invalid PassPhrase.
        VOUCHER_NUM	Unique number of returned e-Voucher contaning 10 digits.	01234567891
        VOUCHER_AMOUNT	Nominal amount of e-Voucher. 
            Also amount that was credited back to your account.	19.95
        Payer_Account	Perfect Money® account of e-Voucher buyer.	U1234567
        PAYMENT_BATCH_NUM	PerfectMoney batch number generated for this transaction. You may query/search account history by this number.	758094

        '''
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
        '''
        Payee_Account	Perfect Money® account to activate e-Voucher to.
        e-Voucher nominal amount was credited to this account.	U1234567
        ev_number	Your Perfect Money® e-Voucher unique number you want to activate.	01234567891
        ev_code	Activation code of e-Voucher.	0123456789123456

        #==========
        # Output
        #==========
        ERROR	e-Voucher was not activated if this field present. Text description of error.	Invalid PassPhrase.
        VOUCHER_NUM	Unique number of activated e-Voucher contaning 10 digits.	01234567891
        VOUCHER_AMOUNT	Nominal amount of e-Voucher. 
            This amount was credited to Payee_Account.	19.95
        Payee_Account	Perfect Money® account of e-Voucher payee.	U1234567
        PAYMENT_BATCH_NUM	PerfectMoney batch number generated for this transaction. You may query/search account history by this number.	758094        
        '''
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