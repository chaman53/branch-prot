const express = require('express');
const router = express.Router();
const UTMCode = require('../../models/UTMCode.js'); // Renamed for clarity and to avoid shadowing

router.get('/utm-codes', async (req, res) => {
    try {
        const utmCodesData = await UTMCode.find().maxTimeMS(30000); // Increased timeout
        res.json(utmCodesData);
    } catch (error) {
        console.error("Error fetching UTM codes:", error);
        if(error.name === 'MongooseError' && error.message.includes('timeout')) {
            res.status(408).json({ message: 'Request Timeout', details: error.message });
        } else {
            res.status(500).json({ message: 'Internal Server Error', details: error.message });
        }
    }
});

module.exports = router;

