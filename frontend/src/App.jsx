// src/App.jsx
import React from "react";
import { Routes, Route } from "react-router-dom";
import RootLayout from "./layouts/RootLayout";
import Landing from "./pages/Landing";
import MainModel from "./pages/mainModel"; // your feature page

export default function App() {
  return (
    <Routes>
      <Route element={<RootLayout />}>
        {/* default: navbar + Home + Contact + footer */}
        <Route index element={<Landing />} />
        {/* feature page */}
        <Route path="feature" element={<MainModel />} />
        {/* optional 404 */}
        <Route path="*" element={<div className="p-6">Not Found</div>} />
      </Route>
    </Routes>
  );
}
