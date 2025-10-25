// src/components/Navbar.jsx
import React from "react";
import { NavLink } from "react-router-dom";

const base = "px-3 py-2 rounded-lg hover:bg-gray-100 transition";
const active = "bg-gray-200";

export default function Navbar() {
  return (
    <header className="bg-white border-b">
      <nav className="max-w-5xl mx-auto p-4 flex gap-2">
        <NavLink to="/" end className={({ isActive }) => `${base} ${isActive ? active : ""}`}>
          Home
        </NavLink>
        <NavLink to="/feature" className={({ isActive }) => `${base} ${isActive ? active : ""}`}>
          Feature
        </NavLink>
      </nav>
    </header>
  );
}
