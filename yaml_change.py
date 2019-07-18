def yaml_input(cus_inp,ord_inp):
### CUSTOMERS :
    cnt=cus_inp
    fp=open("mongofake/customers.yaml","r+")
    contents=fp.read()
    fp.seek(0)
    fp.truncate()
    
    contents=contents.split('\n')
    contents[5]='  count: {}'.format(cnt)
    contents[153]='        build: "return \'order:::\'+Math.floor((Math.random() * {}) + 1);"'.format(ord_inp-1)
    fp.seek(0)
    contents="\n".join(contents)
    fp.write(contents)

    fp.close()          


### ORDERS:
    cnt=ord_inp
    fp=open("mongofake/orders.yaml","r+")
    contents=fp.read()
    fp.seek(0)
    fp.truncate()
    contents=contents.split('\n')
    contents[5]='  count: {}'.format(cnt)
    fp.seek(0)
    contents="\n".join(contents)
    fp.write(contents)
    fp.close()          

yaml_input(1500, 300)