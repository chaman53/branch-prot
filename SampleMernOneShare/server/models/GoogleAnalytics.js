const mongoose = require('mongoose');

const googleAnalyticsSchema = new mongoose.Schema({
    page_path: { type: String, required: true },
    page_title: { type: String, required: true },
    page_views: { type: Number, required: true },
    unique_page_views: { type: Number, required: true },
    avg_time_on_page: { type: Number, required: true },
    entrances: { type: Number, required: true },
    bounce_rate: { type: Number, required: true },
    exit_rate: { type: Number, required: true }
});

const GoogleAnalytics = mongoose.model('google_analytics', googleAnalyticsSchema);

module.exports = GoogleAnalytics;