import { useEffect, useState } from "react";
import { io } from "socket.io-client";
import React from "react";
import "./App.css";

export default function Control() {
  const socket = io("127.0.0.1:5000");

  useEffect(() => {
    document.addEventListener("keydown", detectKeyDown, true);
  }, []);

  const [lastKey, setLastKey] = useState("");

  var detectKeyDown = (e) => {
    console.log(e.key);
    socket.emit("key_pressed", e.key);
    setLastKey(e.key);
  };

  function sendMessage() {
    socket.emit("message", "hello from client");
  }

  socket.on("message", (data) => {
    console.log(data);
  });

  socket.on("response", (data) => {
    console.log(data);
  });

  return (
    <div>
      <button onClick={sendMessage}>Send Message</button>
      <p>
        <b>Last Action:</b> {lastKey}
      </p>
    </div>
  );
}
