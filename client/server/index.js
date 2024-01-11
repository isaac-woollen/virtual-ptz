/* eslint-disable no-undef */
const express = require("express");
const app = express();
const http = require("http");
const { resolve } = require("path");
const fs = require("fs");
const cors = require("cors");

config = require("./config.json");

app.get("/config", (req, res) => {
  res.json(config);
});

app.use(cors());

let STATIC = resolve(__dirname, "dist");

app.use(express.static(STATIC));

const server = http.createServer(app);

const serverAddress = config["vptz-ip"];
const port = 3001;

server.listen(port, () => {
  console.log(`Server is running at http://${serverAddress}:${port}`);
});
