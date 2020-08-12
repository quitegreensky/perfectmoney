# PerfectMoney API

Perfect Money is a financial service allowing the users to make instant payments. This package is inspired by official API [documentations](https://perfectmoney.com/documents/perfectmoney-api.doc) and contains all functions for interacting with PerfectMoney's API as mentioned in documentations.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install package:

```bash
# Latest version
pip install perfectmoney

# Latest changes 
pip install git+https://github.com/quitegreensky/perfectmoney.git
```

## Usage Examples
Here are some examples:
```
from perfectmoney import PerfectMoney
p= PerfectMoney('login_id', 'password') 
#============
# get balance
#============
balance= p.balance()
if not balance:
    print(p.error)
else:
    print(balance)
#returns a dictionary of addresses
#{
#    'USD': [{'U12345': '100.00'}], 
#    'EUR': [{'E12345': '50.00'}], 
#    'GOLD': [{'G12345': '35.00'}, {'G123456785': '0.00'}], 
#    'BTC': [{'B123456785': '0.00'}]
#}

#============
# send money
#============
send= p.spend(payer_account='U123456', Payee_Account='U654321', amount=100)
if not send:
    print(p.error)
else:
    print(send)
# returns 
#{
#    'Payee_Account_Name': 'someaccount', 
#    'Payee_Account': 'U654321', 
#    'Payer_Account': 'U123456', 
#    'PAYMENT_AMOUNT': '1.4', 
#    'PAYMENT_BATCH_NUM': '1234567', 
#    'PAYMENT_ID': ''
#}

#============
# rates
#============
rate = p.rates(currency='EUR')
if not rate :
    print(p.error)
else :
    print(rate)
# returns
#{
#    'time': '8/12/20 4:23:34 AM', 
#    'USD': ' 1.17 ', 
#    'GOLD': ' 0.0006227 ', 
#    'BTC': ' 0.0001045 '
#}
   
```
 
## Contributing


## License
[MIT](https://choosealicense.com/licenses/mit/)