import { useRef, useEffect } from "react";
import FileUpload from "./FileUpload";

function ChatArea({  
  messages,
  input,
  setInput,
  handleSend,
  isLoading,
  handleFileUpload,
  pendingImage,
  clearPendingImage,
}) {
  const bottomRef = useRef(null);

  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  return (
    <div className="h-[calc(100dvh-15rem)] flex flex-col flex-1 bg-[var(--color-bg)] text-white p-10 rounded-lg shadow-xl">
      
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages?.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div //user text
              className={`max-w-[100%] rounded-lg px-4 py-3 ${
                message.role === 'user'
                  ? 'bg-[var(--color-secondary)] text-black'
                  : message.isError
                  ? 'bg-red-100 text-red-800 border border-red-300'
                  : 'bg-[var(--color-button)] text-white font-semi-bold'
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{message.content}</p>

              {/* If user message included an image, show it under the text */}
              {message.image && (
                <div className="mt-2">
                  <img src={message.image} alt="user-upload" className="max-w-xs rounded shadow-md" />
                </div>
              )}

              {/* Show Design Results */}
              {message.designData && (
                <DesignResults data={message.designData} />
              )}
            </div>
          </div>
        ))}

        {/* Loading Indicator */}
        {isLoading && (
          <div className="w-full flex justify-start">
            <div className="bg-[var(--color-button)] rounded-lg px-4 py-3 flex items-center space-x-3">
              <div className="animate-spin h-5 w-5 border-3 border-blue-500 border-t-transparent rounded-full"></div>
              <span className="text-sm text-white font-semi-bold">
                Coordinating 5 AI agents...
              </span>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input Form */}
      {/* Preview of pending image (before send) */}
      {pendingImage && (
        <div className="p-2">
          <div className="flex items-center space-x-3  p-2 rounded">
            <img src={pendingImage} alt="preview" className="h-20 w-28 object-cover rounded" />
          </div>
        </div>
      )}

      <form
        onSubmit={handleSend}
        className="p-2 bg-[var(--color-bg)] flex items-center gap-1 text-black rounded-md border-t border-gray-700"
      >
        <input
          type="text"
          placeholder="Describe your dream space..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={isLoading}
          className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-black disabled:bg-gray-200"
        />
        
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          className="bg-[var(--color-secondary)] text-black px-4 py-2 rounded-lg hover:bg-[var(--color-button)] hover:text-white disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? '⏳' : 'Send'}
        </button>

        <FileUpload onFileUpload={handleFileUpload} />
      </form>
    </div>
  );
}

// Component to display design results
function DesignResults({ data }) {
  const { agent_outputs, confidence_scores } = data;

  return (  // TODO FIX THIS DESIGN
    <div className=" mt-4 space-y-3 bg-[var(--color-button)] p-4">
      {/* <h3 className="font-bold text-lg text-white">✨ Design Complete!</h3> */}

      {/* Style */}
      {agent_outputs?.style_analysis && (
        <div className=" p-3 rounded border border-[var(--color-bg)]">
          <h3 className="font-semibold text-[var(--color-bg)]">Style</h3>
          <p className="text-sm text-[var(--color-bg)] mt-1">
            {agent_outputs.style_analysis.primary_style} • {agent_outputs.style_analysis.mood}
          </p>
        </div>
      )}

      {/* Products */}
      {agent_outputs?.product_recommendations && (
        <div className=" p-3 rounded border border-[var(--color-bg)]">
          <h3 className="font-semibold text-[var(--color-bg)]">Products</h3>
          <p className="text-sm text-[var(--color-bg)]">
            ${agent_outputs.product_recommendations.total_estimated_cost?.toFixed(2)}
          </p>
          <ul className="mt-1 space-y-1">
            {agent_outputs.product_recommendations.selected_products?.slice(0, 3).map((p, i) => (
              <li key={i} className="text-xs text-[var(--color-bg)]">• {p.name}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Budget */}
      {agent_outputs?.budget_analysis && (
        <div className=" p-3 rounded border border-[var(--color-bg)]">
          <h3 className="font-semibold text-[var(--color-bg)]">Budget</h3>
          <p className="text-sm text-[var(--color-bg)]">
            {agent_outputs.budget_analysis.budget_status}
            {agent_outputs.budget_analysis.budget_remaining && 
              ` • $${agent_outputs.budget_analysis.budget_remaining.toFixed(2)} remaining`
            }
          </p>
        </div>
      )}
    </div>
  );
}

export default ChatArea;