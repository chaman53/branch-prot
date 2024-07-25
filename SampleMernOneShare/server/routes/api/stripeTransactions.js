const express = require('express');
const router = express.Router();
const StripeTransaction = require('../../models/StripeTransaction.js'); // Ensure the path to your model file is correct

router.get('/stripe-transactions', async (req, res) => {
    console.log("Accessing the /api/stripe-transactions endpoint");
    try {
        const stripeTransactionsData = await StripeTransaction.find({});
        console.log("Data retrieved:", stripeTransactionsData);
        res.json(stripeTransactionsData);
    } catch (error) {
        console.error("Error occurred:", error.message);
        res.status(500).json({ message: error.message });
    }
});

module.exports = router;