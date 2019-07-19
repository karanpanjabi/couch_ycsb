var couchbase = require('couchbase');

const Fakeit = require('fakeit').default;

const fakeit = new Fakeit();

var host = process.env.COUCH_HOST || "127.0.0.1";
var username = process.env.COUCH_BUCKET || "Administrator";     //the java driver in ycsb doesn't have option for username, but it works if username=bucketname
var password = process.env.COUCH_PASS || "qwerty";
var bucket = process.env.COUCH_BUCKET || "Administrator";

var numDocsPerCustomer = process.env.NUM_DOCS_PER_CUSTOMER || 5;


var cluster = new couchbase.Cluster(`couchbase://${host}`);
cluster.authenticate(username, password);
var bucket = cluster.openBucket(bucket);
console.log("Flushing bucket");
bucket.manager().flush(async function(err, hasCompleted) {
    if (err) {
        console.error(err);
        process.exit(1);
    }
    if (hasCompleted) {
        await insertData();
    }
});

const insertData = async function () {
    var cdata = await fakeit.generate(__dirname + '/customers.yaml');
    cdata = JSON.parse(cdata);

    var ctr = 0;

    for (var customer of cdata) {
        var order_count = Math.floor(Math.random() * (numDocsPerCustomer - 1)) + 1;

        for (var i = 1; i <= order_count; i++) {
            var odata = await fakeit.generate(__dirname + '/orders.yaml');
            odata = JSON.parse(odata);
            odata[0]['_id'] = `order_${i}_${customer['_id']}`;
            customer['order_list'].push(odata[0]['_id']);

            bucket.insert(odata[0]['_id'], odata[0], (err, result) => {
                if(err) {
                    throw err;
                }
            });
        }

        bucket.insert(customer['_id'], customer, (err, result) => {
            if(err) {
                console.log(err);
                process.exit(1);
            }
            if(result) {
                ctr++;
                if(ctr == cdata.length) {
                    console.log("Inserted documents");
                    process.exit(0);
                }
            }
                
        });

        
    }
}