const mongoose = require('mongoose');

const dunyaSchema = new mongoose.Schema({
  streamName: String,
  tickerImagePath: String,
  tickerImage: Buffer,
  uploadDate: Date,
  uploadTime: String,
  ocrText: String,
});

const Dunya = mongoose.model('DunyaTicker', dunyaSchema);

module.exports = Dunya;
