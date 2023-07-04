import { useCallback, useEffect, useState } from "react";
import { io } from "socket.io-client";
import Navbar from "./Navbar";
import Status from "./Status";

const keyCodeActions: any = {
  37: "left",
  38: "up",
  39: "right",
  40: "down",
};

const socket = io("127.0.0.1:5000");

export default function Control() {
  const [lastKey, setLastKey] = useState("");
  const [xPOS, setXPOS] = useState(0.0);
  const [yPOS, setYPOS] = useState(0.0);

  useEffect(() => {
    document.addEventListener("keydown", detectKeyDown, true);
  }, []);

  const updateState = useCallback(async () => {
    socket.emit("info", socket.id);
  }, []);

  useEffect(() => {
    setInterval(updateState, 50);
  }, [updateState]);

  let currentKey = "";

  const detectKeyDown = (e: any) => {
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
  }

  function sendMessage() {
    socket.emit("info", socket.id);
  }

  socket.on("info", (data: string) => {
    const status = JSON.parse(data);
    setXPOS(status["xPOS"]);
    setYPOS(status["yPOS"]);
  });

  return (
    <div className="dark:text-slate-200">
      <Navbar />
      <Status lastAction={lastKey} xPOS={xPOS} yPOS={yPOS} />
      <button onClick={sendMessage}>Button</button>
    </div>
  );
}
