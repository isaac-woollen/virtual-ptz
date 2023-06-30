import React from "react";
import ReactDOM from "react-dom/client";
import App from "./Control";
import "../node_modules/@picocss/pico/css/pico.css";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
