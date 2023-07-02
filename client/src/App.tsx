import { useEffect, useState } from "react";
import { io } from "socket.io-client";
import "./App.css";

const keyCodeActions: any = {
  37: "left",
  38: "up",
  39: "right",
  40: "down",
};

const socket = io("127.0.0.1:5000");

export default function Control() {
  useEffect(() => {
    document.addEventListener("keydown", detectKeyDown, true);
  }, []);

  const [lastKey, setLastKey] = useState("");
  const [info, setInfo] = useState("");

  const detectKeyDown = (e: any) => {
    console.log(e.key);
    socket.emit("key_pressed", e.key);
    setLastKey(e.key);
    sendAction(e.keyCode);
  };

  function sendAction(keyCode: number) {
    const action = keyCodeActions[keyCode];
    if (action != undefined) socket.emit("action", action);
  }
  function sendMessage() {
    socket.emit("info", socket.id);
  }

  socket.on("info", (data) => {
    setInfo(data);
    console.log(data);
  });

  socket.on("response", (data) => {
    console.log(data);
  });

  return (
    <div>
      <button onClick={sendMessage}>Send Message</button>
      <div>{info}</div>
    </div>
  );
}
