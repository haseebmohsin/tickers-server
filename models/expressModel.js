const mongoose = require('mongoose');

const expressSchema = new mongoose.Schema({
  streamName: String,
  tickerImagePath: String,
  tickerImage: Buffer,
  uploadDate: Date,
  uploadTime: String,
  ocrText: String,
});

const Express = mongoose.model('ExpressTicker', expressSchema);

module.exports = Express;
