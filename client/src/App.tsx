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

const configURL = "http://" + self.location.host + "/config";

//const socket = io("http://192.168.1.161:7777");

export default function Control() {
  const [lastAction, setLastAction] = useState("");
  const [xPOS, setXPOS] = useState(0.0);
  const [yPOS, setYPOS] = useState(0.0);
  const [isOnline, setIsOnline] = useState(false);
  const [xSpeed, setXSpeed] = useState(0);
  const [ySpeed, setYSpeed] = useState(0);
  let socket: any;

  function startSocket(url: string) {
    const newSocket = io(url);

    newSocket.on("connect", () => {
      setIsOnline(true);
    });

    newSocket.on("disconnect", () => {
      setIsOnline(false);
    });

    newSocket.on("info", (data: string) => {
      const status = JSON.parse(data);
      setXPOS(status["xPOS"]);
      setYPOS(status["yPOS"]);
      setXSpeed(status["xSpeed"]);
      setYSpeed(status["ySpeed"]);
    });

    newSocket.on("action", (data: string) => {
      setLastAction(data);
    });

    return newSocket;
  }

  useEffect(() => {
    document.addEventListener("keydown", detectKeyDown, true);
    fetch(configURL)
      .then((result) => result.json())
      .then((data) => {
        const vptzURL = `http://${data["vptz-ip"]}:${data["vptz-port"]}`;
        socket = startSocket(vptzURL);
      });
  }, []);

  const updateState = useCallback(async () => {
    socket.emit("info", socket.id);
  }, []);

  useEffect(() => {
    setInterval(updateState, 50);
  }, [updateState]);

  let currentKey = "";

  const detectKeyDown = (e: any) => {
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

  return (
    <div className="dark:text-slate-200">
      <Navbar isOnline={isOnline} />
      <Status
        lastAction={lastAction}
        xPOS={xPOS}
        yPOS={yPOS}
        xSpeed={xSpeed}
        ySpeed={ySpeed}
      />
    </div>
  );
}
