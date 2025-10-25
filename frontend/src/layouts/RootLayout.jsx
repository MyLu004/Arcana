// src/layouts/RootLayout.jsx
import React from "react";
import { Outlet } from "react-router-dom";
import Navbar from "../components/Navbar";

export default function RootLayout() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50 text-gray-900">
      {/* Shared top navigation */}
      <Navbar />

      {/* Page content changes here based on the current route */}
      <main id="content" className=" w-screen">
        {/* Optional container for consistent page width */}
        <div className="max-w-5xl mx-auto w-full p-6">
          <Outlet />
        </div>
      </main>

     
      
    </div>
  );
}
