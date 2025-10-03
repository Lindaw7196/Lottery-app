// lottery-backend/server.js
const express = require("express");
const bodyParser = require("body-parser");
const db = require("./db");
require("dotenv").config();

const app = express();
app.use(bodyParser.json());

// Add participant
app.post("/api/join", async (req, res) => {
  const { name, email } = req.body;
  if (!name || !email) {
    return res.status(400).json({ error: "Name and email required" });
  }
  const ticket = await db.addParticipant(name, email);
  res.json(ticket);
});

// Draw winner (admin only)
app.post("/api/draw", async (req, res) => {
  const { password } = req.body;
  if (password !== process.env.ADMIN_PASSWORD) {
    return res.status(403).json({ error: "Unauthorized" });
  }
  const winner = await db.drawWinner();
  res.json(winner);
});

// List participants
app.get("/api/participants", async (req, res) => {
  const list
