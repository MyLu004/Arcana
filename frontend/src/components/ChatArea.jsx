import {  useRef, useEffect } from "react";

//import { marked } from "marked";    // Converts Markdown to HTML
//import DOMPurify from "dompurify";  // Sanitizes HTML to prevent XSS

// Helper function to parse markdown text and sanitize it
// function parseMarkdown(text) {
//   if (!text) return "";
//   return DOMPurify.sanitize(marked(text)); // convert and clean user input
// }

function ChatArea({  
  messages,           // list of the chat message 
  input,              // input filed state
  setInput,           // function to update input
  handleSend,         // function to handle message send
  isLoading,          // boolean indicating if bot is processing
  
  //handleFileUpload,   // Function to handle file uploads
  //pendingFile,        // Currently selected file (if any)
  //setPendingFile,     // Function to cler selected file
}) {
  
  const bottomRef = useRef(null); // reference to scroll to bottom

  // scroll to bottm effect (scroll to bottol when chat reach the window limit)
  useEffect(() => {
  if (bottomRef.current) {
    bottomRef.current.scrollIntoView({ behavior: "smooth" });
  }
}, [messages]);

  return (
    <div className="h-[calc(100dvh-15rem)] flex flex-col flex-1 bg-[var(--color-bg)] text-white p-10">

       {/* Message history area */}
      <div className="flex-1 overflow-y-auto p-6  space-y-4">

        <div ref={bottomRef} />

      </div>

      <form
        onSubmit={handleSend}
        className="p-2 bg-[var(--color-bg)] flex items-center gap-1 text-black rounded-md"
      >       

        {/* Text input field */}
        <input
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={isLoading}
          className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
        />
        
        {/* Submit button */}
        <button
          type="submit"
          disabled={isLoading}
          className="bg-[var(--color-secondary)] text-black px-4 py-2 rounded-lg hover:bg-[var(--color-button)] hover:text-white"
        >
          Send
        </button>

        {/* <FileUpload onFileUpload={handleFileUpload} /> */}

      </form>
    </div>
  );
}

export default ChatArea;