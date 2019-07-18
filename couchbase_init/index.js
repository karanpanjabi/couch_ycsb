var couchbase = require('couchbase');

var host = process.env.COUCH_HOST || "127.0.0.1";
var username = process.env.COUCH_BUCKET || "Administrator";     //the java driver in ycsb doesn't have option for username, but it works if username=bucketname
var password = process.env.COUCH_PASS || "qwerty";
var bucket = process.env.COUCH_BUCKET || "Administrator";   

var cluster = new couchbase.Cluster(`couchbase://${host}`);
cluster.authenticate(username, password);
var bucket = cluster.openBucket(bucket);
console.log("Flushing bucket");
bucket.manager().flush((err, hasCompleted) => {
    if(err) {
        console.error(err);
        process.exit(1);
    }
    if(hasCompleted) {
        process.exit(0);
    }
});
