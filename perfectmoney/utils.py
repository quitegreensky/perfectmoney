def csv_to_list(csv):
    history= []
    csv= csv.split('\n')
    keys= csv[0].split(',')
    for items in csv[1:-1]:
        items= items.split(',')
        history.append(
            {key:val for key,val in zip(keys,items)}
        )
    return history


def rates_to_dic(currency, rates):
    rates= rates.split(',')
    time= rates[0]
    rates= rates[1:]

    dic= {}
    dic['time']= time
    if currency=='USD':
        dic['EUR']= rates[0]
        dic['GOLD']= rates[1]
        dic['BTC']= rates[2]

    elif currency=='EUR':
        dic['USD']= rates[0]
        dic['GOLD']= rates[1]
        dic['BTC']= rates[2]

    elif currency=='BTC':
        dic['EUR']= rates[0]
        dic['USD'] = rates[1]

    elif currency=='GOLD':
        dic['USD']= rates[0]
        dic['EUR'] = rates[1]            

    return dic
