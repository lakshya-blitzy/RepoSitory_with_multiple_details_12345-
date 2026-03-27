// server.js — Express.js Application Entry Point
// A minimal Node.js server with two GET endpoints using Express.js v5

const express = require('express');

// Create the Express application instance
const app = express();

// Port configuration — respects the PORT environment variable, defaults to 3000
const PORT = process.env.PORT || 3000;

// Route 1: GET / — Returns "Hello world"
app.get('/', (req, res) => {
  res.send('Hello world');
});

// Route 2: GET /evening — Returns "Good evening"
app.get('/evening', (req, res) => {
  res.send('Good evening');
});

// Start the HTTP server and log a confirmation message
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

// Export the Express app instance for testing (e.g., server.test.js)
module.exports = app;
