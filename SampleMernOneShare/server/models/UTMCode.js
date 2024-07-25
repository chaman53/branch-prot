// models/UTMCode.js
const mongoose = require('mongoose');

const utmCodeSchema = new mongoose.Schema({
    id: Number,
    utm_source: { type: String, required: true },
    utm_medium: { type: String, required: true },
    utm_campaign: { type: String, required: true },
    utm_term: { type: String, required: true },
    utm_content: { type: String, required: true },
    visits: { type: Number, required: true }
}, { timestamps: true });

const UTMCode = mongoose.model('utm_codes', utmCodeSchema);

module.exports = UTMCode;