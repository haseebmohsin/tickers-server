const mongoose = require('mongoose');

const geoSchema = new mongoose.Schema({
  streamName: String,
  tickerImagePath: String,
  tickerImage: Buffer,
  uploadDate: Date,
  uploadTime: String,
});

const Geo = mongoose.model('GeoTicker', geoSchema);

module.exports = Geo;
