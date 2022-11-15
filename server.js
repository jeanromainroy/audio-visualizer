'use strict';

// config
const API_PORT = 8080;

// libs
import express from 'express';

// instantiate express server
const app = express();

// enable parse body
app.use(express.json());

// enable serving static files through client folder
app.use(express.static('./public'));

// start server
app.listen(API_PORT, () => {
    console.log(`\naudio visualizer hosted at http://localhost:${API_PORT}\n`);
});
