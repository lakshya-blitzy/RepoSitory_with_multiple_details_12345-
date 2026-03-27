// server.test.js — Unit/Integration Tests for Express.js Endpoints
// Validates both GET / and GET /evening endpoints return correct HTTP 200
// responses with the exact expected body strings.
//
// Usage: node server.test.js
//        npm test

const http = require('http');
const assert = require('assert');

// ---------------------------------------------------------------------------
// Test Configuration
// ---------------------------------------------------------------------------
// Use a dedicated test port to avoid conflicts with any running services.
// This must be set BEFORE requiring server.js, because server.js reads
// process.env.PORT at module load time to bind its listener.
const TEST_PORT = 3456;
process.env.PORT = TEST_PORT;

// Import the Express application instance from server.js.
// Requiring this module triggers app.listen(), which starts the HTTP server
// on TEST_PORT so the endpoints are available for integration testing.
const app = require('./server');

// ---------------------------------------------------------------------------
// Helper: httpGet(path)
// ---------------------------------------------------------------------------
// Makes an HTTP GET request to the test server at the specified path.
// Returns a Promise that resolves with an object containing the numeric
// HTTP status code and the full response body as a string.
//
// @param {string} path - The URL path to request (e.g., '/' or '/evening')
// @returns {Promise<{statusCode: number, body: string}>}
// ---------------------------------------------------------------------------
function httpGet(path) {
  return new Promise(function (resolve, reject) {
    var url = 'http://localhost:' + TEST_PORT + path;

    http.get(url, function (res) {
      var body = '';

      res.on('data', function (chunk) {
        body += chunk;
      });

      res.on('end', function () {
        resolve({ statusCode: res.statusCode, body: body });
      });
    }).on('error', function (err) {
      reject(err);
    });
  });
}

// ---------------------------------------------------------------------------
// Test Runner
// ---------------------------------------------------------------------------
// Executes all test cases sequentially, tracks pass/fail counts, and prints
// a summary. Exits with code 0 when every test passes or code 1 when any
// test fails, ensuring CI pipelines and npm scripts report the correct status.
// ---------------------------------------------------------------------------
async function runTests() {
  var passed = 0;
  var failed = 0;

  console.log('');
  console.log('===========================================');
  console.log(' server.test.js — Express Endpoint Tests');
  console.log('===========================================');
  console.log('');

  // -----------------------------------------------------------------
  // Test Case 1: GET / should return HTTP 200 with body "Hello world"
  // -----------------------------------------------------------------
  try {
    var response1 = await httpGet('/');

    assert.strictEqual(
      response1.statusCode,
      200,
      'GET / — Expected HTTP status 200 but received ' + response1.statusCode
    );

    assert.strictEqual(
      response1.body,
      'Hello world',
      'GET / — Expected body "Hello world" but received "' + response1.body + '"'
    );

    console.log('  ✓ PASS — GET / returns 200 with body "Hello world"');
    passed++;
  } catch (err) {
    console.error('  ✗ FAIL — GET /');
    console.error('    Reason: ' + err.message);
    failed++;
  }

  // -----------------------------------------------------------------
  // Test Case 2: GET /evening should return HTTP 200 with body "Good evening"
  // -----------------------------------------------------------------
  try {
    var response2 = await httpGet('/evening');

    assert.strictEqual(
      response2.statusCode,
      200,
      'GET /evening — Expected HTTP status 200 but received ' + response2.statusCode
    );

    assert.strictEqual(
      response2.body,
      'Good evening',
      'GET /evening — Expected body "Good evening" but received "' + response2.body + '"'
    );

    console.log('  ✓ PASS — GET /evening returns 200 with body "Good evening"');
    passed++;
  } catch (err) {
    console.error('  ✗ FAIL — GET /evening');
    console.error('    Reason: ' + err.message);
    failed++;
  }

  // -----------------------------------------------------------------
  // Test Summary
  // -----------------------------------------------------------------
  console.log('');
  console.log('-------------------------------------------');
  console.log(' Results: ' + passed + ' passed, ' + failed + ' failed, ' + (passed + failed) + ' total');
  console.log('-------------------------------------------');
  console.log('');

  // Exit with the appropriate status code so that npm test and CI systems
  // correctly interpret the outcome. Code 0 = success, Code 1 = failure.
  process.exit(failed > 0 ? 1 : 0);
}

// ---------------------------------------------------------------------------
// Execution Entry Point
// ---------------------------------------------------------------------------
// A brief delay allows the Express server (started by requiring server.js
// above) to finish binding to the test port before the first HTTP request
// is made. 200 ms is more than sufficient for a local TCP bind.
setTimeout(runTests, 200);
