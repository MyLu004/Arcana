// src/pages/Landing.jsx
import React from "react";
import Home from "./Home";
import Contact from "./Contact";
import Footer from "../components/Footer";


export default function Landing() {
  return (
    <div className="h-[calc(100dvh-15rem)]">
      <Home />
      <Contact />
      {/* <Footer /> */}
    </div>
  );
}
