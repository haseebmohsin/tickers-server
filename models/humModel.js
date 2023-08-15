const mongoose = require('mongoose');

const humSchema = new mongoose.Schema({
  streamName: String,
  tickerImagePath: String,
  tickerImage: Buffer,
  uploadDate: Date,
  uploadTime: String,
});

const Hum = mongoose.model('HumTicker', humSchema);

module.exports = Hum;
