// services/booksService.js
const Book = require('../entities/bookModel');

const getBooks = async () => {
  try {
    const books = await Book.find();
    return books;
  } catch (error) {
    throw new Error('Failed to fetch books');
  }
};

module.exports = {
  getBooks,
};
