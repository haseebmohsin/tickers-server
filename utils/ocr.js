const tesseract = require('tesseract.js');

async function extractTickerText(imagePath) {
  // Pass the language code as an option
  const result = await tesseract.recognize(imagePath, 'urd');
  return result.data.text;
}

module.exports = {
  extractTickerText,
};
