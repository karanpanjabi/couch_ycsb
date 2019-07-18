Since there are three stages to get YCSB running the first file that gets executed is init.py

init.py reads info about customer_count, order_count and server connection info, and makes the respective changes in the yaml files and then executes the fakeit part (in nodejs) which loads the data onto the database server, and the load and run phases of YCSB.

A sample command is given below:

docker run -it --rm --network host -v /home/karan/Documents/ccbd/test_workloads:/home/user/test_workloads -e "WORKLOAD_PATH=/home/user/test_workloads/workloadssearch" karanpanjabikp/couch_ycsb

The container needs to be connected to the appropriate network in order to connect to server. In order to specify the workload file, one needs to specify the WORKLOAD_PATH environment variable. I've mounted the directory containing the workloads in my host to some folder in the container and then specified the workload file workloadssearch.

For compatibility and readability with legacy code, we've specified three params for workload file: recordcount, totalrecordcount, and customer_count which refer to the same number. There is also order_count which refers to the number of order documents that need to be inserted. The other important params are couchbase.host, couchbase.bucket and couchbase.password. Due to old couchbase drivers being used in YCSB, the username should be same as bucketname. So, I had username Administrator with password qwerty, so I made a bucket name Administrator. So my configuration was: couchbase.host=127.0.0.1 couchbase.password=qwerty couchbase.bucket=Administrator

Follow the instructions at https://github.com/couchbaselabs/YCSB/blob/soe/couchbase2/README.md for setting up the index and for more info on the properties that can be set. These params are necessary in order to make sure the code works.
