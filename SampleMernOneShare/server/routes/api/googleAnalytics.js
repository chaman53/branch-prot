const express = require('express');
const router = express.Router();
const GoogleAnalytics = require('../../models/GoogleAnalytics.js'); // Ensure the path to your model file is correct

router.get('/google-analytics', async (req, res) => {
    try {
        const analyticsData = await GoogleAnalytics.find({});
        res.json(analyticsData);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

module.exports = router;