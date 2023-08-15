const mongoose = require('mongoose');

const samaaSchema = new mongoose.Schema({
  streamName: String,
  tickerImagePath: String,
  tickerImage: Buffer,
  uploadDate: Date,
  uploadTime: String,
});

const Samaa = mongoose.model('SamaaTicker', samaaSchema);

module.exports = Samaa;
