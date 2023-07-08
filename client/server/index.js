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

server.listen(3001, () => {
  console.log("Server is running on port 3001");
});
