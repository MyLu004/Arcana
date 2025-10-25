// src/pages/mainModel.jsx
import React from "react";
import SideBar from "../components/SideBar";
import ChatArea from "../components/ChatArea";
import { useChat } from "../hooks/useChat";

const placeholder =
  "https://images.unsplash.com/photo-1519710164239-da123dc03ef4?q=80&w=1200&auto=format&fit=crop";

export default function MainModel({ className = "" }) {
  // Use our custom chat hook
  const { 
    messages, 
    input, 
    setInput, 
    isLoading, 
    handleSend, 
    handleFileUpload,
    onNewChat 
  } = useChat();

  return (
    <div className={`flex h-[calc(100dvh-10rem)] ${className}`}>
      <SideBar 
        onNewChat={onNewChat}
        onOpenCad={() => console.log('CAD feature coming soon')}
      />

      <main className="flex-1 min-w-0 p-6 md:p-10">
        <div className="mx-auto max-w-6xl">
          <ChatArea
            messages={messages}
            input={input}
            setInput={setInput}
            handleSend={handleSend}
            isLoading={isLoading}
            handleFileUpload={handleFileUpload}
            imageSrc={placeholder}
          />
        </div>
      </main>
    </div>
  );
}