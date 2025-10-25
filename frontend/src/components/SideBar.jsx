// SideBar.jsx
import React from "react";

export default function SideBar({
  onNewChat,
  onOpenCad,
  className = "",
}) {
  return (
    <aside
      className={`w-64 shrink-0 border-r border-slate-300 bg-[var(--bg-color)] min-h-screen px-3 py-4 ${className}`}
    >
      <div className="space-y-3">
        <button
          onClick={onNewChat}
          className="w-full rounded-md border border-slate-400 px-4 py-3 text-sm font-medium tracking-wide shadow-sm hover:bg-white"
        >
          new chat
        </button>

        <button
          onClick={onOpenCad}
          className="w-full rounded-md border border-slate-400 px-4 py-3 text-sm font-medium tracking-wide shadow-sm hover:bg-white"
        >
          gemetric CAD feature
        </button>
      </div>

      <div className="my-6 h-px w-full bg-slate-300" />

      {/* Add any extra sidebar content here */}
    </aside>
  );
}
