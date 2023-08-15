const express = require('express');
const router = express.Router();
const { processLivestream, getLiveTickers } = require('../controllers/livestreamController');

// GET /api/livestream/processLivestream
router.get('/processLivestream', processLivestream);

// GET /api/livestream/getLiveTickers
router.get('/getLiveTickers', getLiveTickers);

module.exports = router;
