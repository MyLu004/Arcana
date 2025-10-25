// src/components/Footer.jsx
import React from "react";
import { Link } from "react-router-dom";

export default function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="border-t bg-white">
      <div className="max-w-5xl mx-auto px-4 py-8 grid gap-6 sm:grid-cols-3">
        {/* Brand */}
        <div className="space-y-2">
          <h2 className="text-lg font-semibold">YourApp</h2>
          <p className="text-sm text-gray-600">
            Build. Ship. Delight.
          </p>
        </div>

        {/* Quick links */}
        <nav className="space-y-2">
          <p className="text-sm font-medium text-gray-700">Pages</p>
          <ul className="space-y-1 text-sm">
            <li>
              <Link className="hover:underline text-gray-700" to="/">Home</Link>
            </li>
            <li>
              <Link className="hover:underline text-gray-700" to="/feature">Feature</Link>
            </li>
            <li>
              <a
                className="hover:underline text-gray-700"
                href="mailto:hello@example.com"
              >
                Contact
              </a>
            </li>
          </ul>
        </nav>

        {/* Newsletter (optional) */}
        <div className="space-y-2">
          <p className="text-sm font-medium text-gray-700">Stay in the loop</p>
          <form
            className="flex gap-2"
            onSubmit={(e) => {
              e.preventDefault();
              alert("Thanks! (wire this up later)");
            }}
          >
            <input
              type="email"
              placeholder="you@example.com"
              className="w-full rounded-lg border px-3 py-2 text-sm focus:outline-none focus:ring"
              required
            />
            <button
              type="submit"
              className="rounded-lg bg-blue-600 px-3 py-2 text-sm text-white hover:bg-blue-700"
            >
              Join
            </button>
          </form>
        </div>
      </div>

      {/* Bottom bar */}
      <div className="border-t">
        <div className="max-w-5xl mx-auto px-4 py-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <p className="text-xs text-gray-500">
            © {year} YourApp. All rights reserved.
          </p>
          <div className="flex items-center gap-4 text-xs text-gray-600">
            <Link to="/privacy" className="hover:underline">Privacy</Link>
            <Link to="/terms" className="hover:underline">Terms</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
