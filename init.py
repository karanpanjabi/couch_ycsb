import os
from urlparse import urlparse
import subprocess

# read the workload file for count properties, mongo url
def read_props(filepath):
    props = {}
    with open(filepath) as wfile:
        lines = wfile.readlines()
        for line in lines:
            line = line.strip()
            if not line.startswith("#") and line.find("=") != -1:
                eidx = line.find("=")
                key = line[0:eidx].strip()
                val = line[eidx+1:].strip()

                props[key] = val
    return props

# call the respective function to make changes in the yaml files
def yaml_input(cus_inp,ord_inp):
### CUSTOMERS :
    cnt=cus_inp
    fp=open("couchbase_init/customers.yaml","r+")
    contents=fp.read()
    fp.seek(0)
    fp.truncate()
    
    contents=contents.split('\n')
    contents[5]='  count: {}'.format(cnt)
    # contents[153]='        build: "return \'order:::\'+Math.floor((Math.random() * {}) + 1);"'.format(ord_inp-1)
    fp.seek(0)
    contents="\n".join(contents)
    fp.write(contents)

    fp.close()          


### ORDERS:
    # cnt=o1   

def syscall(cmd):
    print("Executing: "+cmd)
    status = os.system(cmd)
    if(status != 0):
        exit(1)

if __name__ == "__main__":
    props = {}
    workloaddirpath = "%s/workloads/" % (os.getcwd())
    workloadpath = workloaddirpath+"workloadsa"    #read from env?

    workloadpath = os.environ.get("WORKLOAD_PATH") or workloadpath

    props = read_props(workloadpath)

    DEFAULT_CUSTOMER_COUNT = 1000
    DEFAULT_ORDER_COUNT = 200

    ccount = int(props.get("customer_count") or props.get("totalrecordcount") or props.get("recordcount") or DEFAULT_CUSTOMER_COUNT)
    ocount = int(props.get("order_count") or DEFAULT_ORDER_COUNT)

    print(ccount, ocount)

    threads_load = 1
    threads_run = 1
    if("threads_load" in props):
        threads_load = int(props["threads_load"])
    if("threads_run" in props):
        threads_run = int(props["threads_run"])

    yaml_input(ccount, ocount)

    os.environ["COUCH_HOST"] = couchhost = props.get("couchbase.host") or "127.0.0.1"
    os.environ["COUCH_BUCKET"] = couchbucket = props.get("couchbase.bucket") or "Administrator"
    os.environ["COUCH_PASS"] = couchpassword = props.get("couchbase.password") or "qwerty"

    print("\n\n--------------------Fakeit: Loading data to DB---------------------------")
    syscall("node couchbase_init/")
    # syscall("fakeit couchbase -s %s -u %s -b %s -p %s fakeit_yaml/customers.yaml" % (couchhost, couchbucket, couchbucket, couchpassword))
    # syscall("fakeit couchbase -s %s -u %s -b %s -p %s fakeit_yaml/orders.yaml" % (couchhost, couchbucket, couchbucket, couchpassword))
    print("\n\n--------------------YCSB: Load phase---------------------------")
    syscall("cd YCSBjson ; bin/ycsb load couchbase2 -s -P %s -threads %d" % (workloadpath, threads_load))
    print("\n\n--------------------YCSB: Run phase---------------------------")
    syscall("cd YCSBjson ; bin/ycsb run couchbase2 -s -P %s -threads %d" % (workloadpath, threads_load))
