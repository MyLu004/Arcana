// src/components/Navbar.jsx
import React from "react";
import { NavLink } from "react-router-dom";

const base = "px-3 py-2 rounded-lg hover:bg-gray-100 transition";
const active = "bg-gray-200";

export default function Navbar() {
  return (
    <header className="bg-[var(--color-bg)] border-b border-black/30">
      <nav className="max-w-5xl mx-auto p-6 flex items-center justify-center gap-4">
        <NavLink to="/" end className={({ isActive }) => `${base} ${isActive ? active : ""} bg-[var(--color-bg)] hover:bg-[var(--color-bg)] group relative inline-flex items-center px-2 py-1 text-zinc-800 transition-transform duration-200
           hover:scale-105 hover:text-zinc-900 focus:outline-none focus-visible:scale-105`}>
          Home

          <span
      className="pointer-events-none absolute inset-x-0 -bottom-0.5 h-[1px] origin-left scale-x-0 rounded
             bg-zinc-900/70 transition-transform duration-200 group-hover:scale-x-100"
      aria-hidden="true"
          ></span>
        </NavLink>
        <NavLink to="/mainModel" className={({ isActive }) => `${base} ${isActive ? active : ""} bg-[var(--color-bg)] hover:bg-[var(--color-bg)] group relative inline-flex items-center px-2 py-1 text-zinc-800 transition-transform duration-200
           hover:scale-105 hover:text-zinc-900 focus:outline-none focus-visible:scale-105`}>
          Feature

          <span
      class="pointer-events-none absolute inset-x-0 -bottom-0.5 h-[1px] origin-left scale-x-0 rounded
             bg-zinc-900/70 transition-transform duration-200 group-hover:scale-x-100"
      aria-hidden="true"
          ></span>

        </NavLink>
      </nav>
    </header>
  );
}
