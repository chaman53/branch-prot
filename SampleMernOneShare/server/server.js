// Import necessary modules
const express = require('express');
//const { MongoClient, ServerApiVersion } = require('mongodb');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

// Routes
const utmCodesRoutes = require('./routes/api/utmCodes');
const stripeTransactionsRoutes = require('./routes/api/stripeTransactions');
const googleAnalyticsRoutes = require('./routes/api/googleAnalytics');
const baseApiRouter = require('./routes/api/index');

// Initialize express app
const app = express();

// Apply middleware
app.use(cors({
  origin: 'http://localhost:3000'  // Adjust depending on your frontend host
}));
app.use(express.json()); // For parsing application/json

// MongoDB connection settings including SSL configuration
const uri = process.env.MONGODB_URI; // Use environment variable for URI
// const client = new MongoClient(uri, {
//   serverApi: {
//     version: ServerApiVersion.v1,
//     strict: true,
//     deprecationErrors: true
//   },
//   tlsAllowInvalidCertificates: true, // To handle invalid SSL certificates
//   tls: true // Ensure TLS is used for the connection
// });

// Port configuration
const PORT = process.env.PORT || 5001;

// Function to connect to MongoDB and start the server
async function connectToMongoDBAndStartServer() {
  try {
await mongoose.connect(uri, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
    serverSelectionTimeoutMS: 30000, // 30 seconds timeout
    socketTimeoutMS: 45000 // 45 seconds socket timeout
  });
    console.log("Connected successfully to MongoDB!");

    //await client.connect();
    //console.log("Connected successfully to MongoDB!");

    // Setup route handlers
    app.use('/api', utmCodesRoutes);
    app.use('/api', stripeTransactionsRoutes);
    app.use('/api', googleAnalyticsRoutes);
    app.use('/api', baseApiRouter);

    app.get('/', (req, res) => {
      res.send('Hello from Express server with MongoDB!');
    });

    // Start listening on specified port
    app.listen(PORT, () => {
      console.log(`Server started on port ${PORT}`);
    });
  } catch (error) {
    console.error("Failed to connect to MongoDB", error);
    process.exit(1); // Exit process if cannot connect to MongoDB
  }
}

// Call the function to connect to MongoDB and start the server
connectToMongoDBAndStartServer();




// const express = require('express');
// const mongoose = require('mongoose');
// const { run } = require('./mongoUtil');
// const cors = require('cors');
// require('dotenv').config();
// const utmCodesRoutes = require('./routes/api/utmCodes'); // Adjust path as necessary
// const stripeTransactionsRoutes = require('./routes/api/stripeTransactions');
// const googleAnalyticsRoutes = require('./routes/api/googleAnalytics');
// const baseApiRouter = require('./routes/api/index.js'); 


// const app = express();
// const PORT = process.env.PORT || 5001;

// app.use(cors());
// app.use(express.json()); // Allows us to parse JSON

// // Route setups
// app.use('/api', utmCodesRoutes);
// app.use('/api', stripeTransactionsRoutes);
// app.use('/api', googleAnalyticsRoutes);
// app.use('/api', baseApiRouter);


// // MongoDB Connection
// mongoose.connect(process.env.MONGODB_URI, {
//     useNewUrlParser: true,
//     useUnifiedTopology: true
// }).then(() => {
//     console.log('MongoDB Connected');
//     // Start the Express server only if MongoDB is connected
//     app.listen(PORT, () => console.log(`Server started on port ${PORT}`));
// }).catch(err => {
//     console.error('Failed to connect to MongoDB', err);
// });

// // Define routes here, e.g., a simple test route
// app.get('/', (req, res) => {
//     res.send('Hello from Express server!');
// });
