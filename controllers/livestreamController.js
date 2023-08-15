const asyncHandler = require('express-async-handler');
const fs = require('fs');
const Geo = require('../models/geoModel');
const Ary = require('../models/aryModel');
const Dunya = require('../models/dunyaModel');
const Samaa = require('../models/samaaModel');
const Hum = require('../models/humModel');
const Express = require('../models/expressModel');
const { extractTickerText } = require('../utils/ocr');
const mongoose = require('mongoose');

const STREAM_URL = process.env.ARY_NEWS_LIVE_STREAM_URL;

/**
 * @desc  live stream processing
 * @route   POST /api/livestream/processLivestream
 * @access  Private
 */
const processLivestream = asyncHandler(async (req, res) => {
  const imageDirectory = 'assets/frames';

  // Read the list of files in the directory
  const imageFiles = fs.readdirSync(imageDirectory);

  for (const imageName of imageFiles) {
    // Construct the image path
    const imagePath = `${imageDirectory}/${imageName}`;

    // Perform OCR on the image
    var extractedText = await extractTickerText(imagePath);

    console.log(`Text from ${imageName}: ${extractedText}`);
  }

  res.status(200).json({ message: 'OCR processing completed', ocrText: extractedText });
});

/**
 * @desc    live stream processing
 * @route   GET /api/livestream/getLiveTickers
 * @access  Private
 */
const getLiveTickers = asyncHandler(async (req, res) => {
  const channel = req.query.channel;

  const collections = [Geo, Dunya, Ary, Express, Hum, Samaa];
  const limitPerCollection = 10;
  let combinedData = [];
  let tickersData = [];

  switch (channel) {
    case 'Geo':
      combinedData = await Geo.find().sort({ _id: -1 }).limit(20);
      break;
    case 'Ary':
      combinedData = await Ary.find().sort({ _id: -1 }).limit(20);
      break;
    case 'Dunya':
      combinedData = await Dunya.find().sort({ _id: -1 }).limit(20);
      break;
    case 'Samaa':
      combinedData = await Samaa.find().sort({ _id: -1 }).limit(20);
      break;
    case 'Hum':
      combinedData = await Hum.find().sort({ _id: -1 }).limit(20);
      break;
    case 'Express':
      combinedData = await Express.find().sort({ _id: -1 }).limit(20);
      break;
    default:
      for (let i = 0; i < limitPerCollection; i++) {
        for (const collection of collections) {
          const data = await collection.find().sort({ _id: -1 }).limit(limitPerCollection);
          if (data[i]) {
            combinedData.push(data[i]);
          }
        }
      }
      break;
  }

  // Convert tickerImage to base64 for each document
  tickersData = combinedData.map((item) => {
    item._id = new mongoose.Types.ObjectId();

    if (item.tickerImage instanceof Buffer) {
      const base64Image = item.tickerImage.toString('base64');
      return {
        ...item.toObject(),
        tickerImage: base64Image,
      };
    }
    return item.toObject();
  });

  res.status(200).json({ message: 'Live Tickers fetched and interleaved', tickersData });
});

module.exports = {
  processLivestream,
  getLiveTickers,
};
