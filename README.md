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
#============
# e-voucher activation
#============
activation= p.voucher_activation(ev_number='123456', ev_code='123456', payee_account='U123456')
if not activation:
    print(p.error)
else:
    print(activation)
#============
# send money
#============
send= p.spend(payer_account='U123456', Payee_Account='U123456', payee_account='U123456', amount=100)
if not send:
    print(p.error)
else:
    print(send)
```
 
## Contributing


## License
[MIT](https://choosealicense.com/licenses/mit/)