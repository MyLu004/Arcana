// MainModel.jsx
import React from "react";
import SideBar from "../components/SideBar";
import ChatArea from "../components/ChatArea";

// If you have the same photo as in the mock, import it here
// import livingRoom from "../assets/living-room.jpg";
const placeholder =
  "https://images.unsplash.com/photo-1519710164239-da123dc03ef4?q=80&w=1200&auto=format&fit=crop";

export default function MainModel({
  onNewChat,
  onOpenCad,
  onSendMessage,
  className = "",
}) {
  return (
    <div className={`flex min-h-screen bg-[#FAF9F6] ${className}`}>
      <SideBar onNewChat={onNewChat} onOpenCad={onOpenCad} />

      <main className="flex-1 p-6 md:p-10">
        <div className="mx-auto max-w-6xl">
          <ChatArea
            imageSrc={placeholder}
            onSend={onSendMessage}
            onHeaderButtonClick={() => {}}
          />
        </div>
      </main>
    </div>
  );
}
