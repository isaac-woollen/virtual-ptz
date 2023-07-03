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

  let currentKey = "";

  const detectKeyDown = (e: any) => {
    console.log(e.key);
    socket.emit("key_pressed", e.key);
    setLastKey(e.key);
    sendKeyAction(e.keyCode);
  };

  function sendKeyAction(keyCode: number) {
    const action = keyCodeActions[keyCode];
    if (currentKey != action) {
      currentKey = action;
      return;
    }
    if (action != undefined) socket.emit("action", action);
    console.log(currentKey);
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
      <div>{info}</div>
    </div>
  );
}
