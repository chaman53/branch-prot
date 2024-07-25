const { MongoClient, ServerApiVersion } = require('mongodb');

// Environment variables for security and flexibility
require('dotenv').config();

const uri = process.env.MONGODB_URI || "mongodb+srv://Cluster19146:<_9ziTq2qK4Bes-f>@mydemocluster0.lyqmb6x.mongodb.net/?appName=MyDemoCluster0";

const client = new MongoClient(uri, {
  serverApi: {
    version: ServerApiVersion.v1,
    strict: true,
    deprecationErrors: true,
  }
});

async function run() {
  try {
    await client.connect();
    await client.db("admin").command({ ping: 1 });
    console.log("Connected successfully to MongoDB!");
  } catch (error) {
    console.error("Could not connect to MongoDB:", error);
  } finally {
    await client.close();
  }
}

module.exports = { run };
