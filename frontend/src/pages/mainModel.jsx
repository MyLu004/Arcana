import React, { useState } from "react";
import SideBar from "../components/SideBar";
import ChatArea from "../components/ChatArea";
import GeometricCad from "../components/GeometricCAD"; // <- fix name/path if needed
import { useChat } from "../hooks/useChat";

const placeholder =
  "https://images.unsplash.com/photo-1519710164239-da123dc03ef4?q=80&w=1200&auto=format&fit=crop";

export default function MainModel({ className = "" }) {
  const {
    messages,
    input,
    setInput,
    budget, 
    setBudget,
    isLoading,
    handleSend,
    handleFileUpload,
    onNewChat,
    pendingImage,
    clearPendingImage,
  } = useChat();

  // "chat" | "cad"
  const [view, setView] = useState("chat");

  // Use this to force ChatArea to remount (fresh state) on New Chat
  const [chatKey, setChatKey] = useState(0);

  const handleNewChat = () => {
    onNewChat?.();           // your hook’s reset (messages, history, etc.)
    clearPendingImage?.();   // clear any staged image
    setInput?.("");          // optional: clear input
    setBudget?.("");
    setChatKey((k) => k + 1); // force ChatArea remount
    setView("chat");         // make sure we’re on the chat view
  };

  return (
    <div className={`flex h-[calc(100dvh-10rem)] ${className}`}>
      <SideBar
        onNewChat={handleNewChat}
        onOpenCad={() => setView("cad")}
      />

      <main className="flex-1 min-w-0 p-6 md:p-10">
        <div className="mx-auto max-w-6xl h-full flex flex-col">
          {/* Header / Switcher */}
          <div className="mb-4 flex items-center gap-2">
            <button
              className={`px-3 py-1 rounded-xl text-sm border ${
                view === "chat" ? "bg-black text-white" : "bg-transparent"
              }`}
              onClick={() => setView("chat")}
            >
              Chat
            </button>
            <button
              className={`px-3 py-1 rounded-xl text-sm border ${
                view === "cad" ? "bg-black text-white" : "bg-transparent"
              }`}
              onClick={() => setView("cad")}
            >
              Geometric CAD
            </button>
          </div>

          {/* Body */}
          <div className="flex-1 min-h-0">
            {view === "chat" ? (
              <ChatArea
                key={chatKey}                 // <- remount on New Chat
                messages={messages}
                input={input}
                setInput={setInput}
                budget={budget} 
                setBudget={setBudget}
                handleSend={handleSend}
                isLoading={isLoading}
                handleFileUpload={handleFileUpload}
                imageSrc={placeholder}
                pendingImage={pendingImage}
                clearPendingImage={clearPendingImage}
              />
            ) : (
              <GeometricCad
                className="h-full"
                onBackToChat={() => setView("chat")}
              />
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
