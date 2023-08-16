const mongoose = require('mongoose');

const arySchema = new mongoose.Schema({
  streamName: String,
  tickerImagePath: String,
  tickerImage: Buffer,
  uploadDate: Date,
  uploadTime: String,
  ocrText: String,
});

const Ary = mongoose.model('AryTicker', arySchema);

module.exports = Ary;
