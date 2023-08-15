const express = require('express');
const livestreamRouter = require('./livestreamRoutes');

const router = express.Router();

// Mount livestream routes
router.use('/livestream', livestreamRouter);

module.exports = router;
