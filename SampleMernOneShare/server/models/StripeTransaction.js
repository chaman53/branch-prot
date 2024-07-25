const mongoose = require('mongoose');

// Define the schema for Stripe transactions
const stripeTransactionSchema = new mongoose.Schema({
    transaction_id: { type: String, required: true, unique: true },
    amount: { type: Number, required: true },
    currency: { type: String, required: true },
    status: { type: String, required: true },
    date: { type: Date, required: true },
    customer_id: { type: String, required: true }
});

// Create the model from the schema
const StripeTransaction = mongoose.model('stripe_transaction', stripeTransactionSchema);

module.exports = StripeTransaction;
