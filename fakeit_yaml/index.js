const Fakeit = require('fakeit').default;

const fakeit = new Fakeit();

const MongoClient = require('mongodb').MongoClient;

var ipport = "localhost:27017";
if(typeof(process.env.MONGO_URL) !== "undefined") {
    ipport = process.env.MONGO_URL;
}
const url = `mongodb://${ipport}`;
var dbName = 'ycsb';
if(typeof(process.env.MONGO_DBNAME) !== "undefined") {
    dbName = process.env.MONGO_DBNAME;
}


MongoClient.connect(url, async function (err, client) {
    if(client) {
        console.log("Fakeit: Connected successfully to server");
    
        const db = client.db(dbName);
        const collection = db.collection('jsondata');
        var numDocs = await collection.countDocuments();
        if(numDocs > 0) {
            await collection.drop();
        }
        await insertDocuments(db);
        client.close();
    }
    else {
        console.error(err.message);
        process.exit(1);
    }
});

const insertDocuments = async function (db) {
    // Get the documents collection
    const collection = db.collection('jsondata');
    var cdata = await fakeit.generate(__dirname+'/customers.yaml');
    cdata = JSON.parse(cdata);
    collection.insertMany( cdata, function (err, result) {
        console.log("Fakeit: Inserted customer documents into the collection");
    });
    
    var odata = await fakeit.generate(__dirname+'/orders.yaml');
    odata = JSON.parse(odata);
    collection.insertMany( odata, function (err, result) {
        console.log("Fakeit: Inserted order documents into the collection");
    });

};
