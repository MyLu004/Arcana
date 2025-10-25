import { useRef, useEffect } from "react";
import FileUpload from "./FileUpload";

function ChatArea({  
  messages,
  input,
  setInput,
  handleSend,
  isLoading,
  handleFileUpload,
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
            <div
              className={`max-w-[85%] rounded-lg px-4 py-3 ${
                message.role === 'user'
                  ? 'bg-[var(--color-secondary)] text-black'
                  : message.isError
                  ? 'bg-red-100 text-red-800 border border-red-300'
                  : 'bg-gray-800 text-gray-100'
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{message.content}</p>

              {/* Show Design Results */}
              {message.designData && (
                <DesignResults data={message.designData} />
              )}
            </div>
          </div>
        ))}

        {/* Loading Indicator */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-800 rounded-lg px-4 py-3 flex items-center space-x-3">
              <div className="animate-spin h-5 w-5 border-3 border-blue-500 border-t-transparent rounded-full"></div>
              <span className="text-sm text-gray-200">
                Coordinating 5 AI agents...
              </span>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input Form */}
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

  return (
    <div className="mt-4 space-y-3 bg-gray-900 p-4 rounded-lg border border-gray-700">
      <h3 className="font-bold text-lg text-white">✨ Design Complete!</h3>

      {/* Style */}
      {agent_outputs?.style_analysis && (
        <div className="bg-purple-900/30 p-3 rounded border border-purple-700">
          <h4 className="font-semibold text-purple-300">🎨 Style</h4>
          <p className="text-sm text-purple-200 mt-1">
            {agent_outputs.style_analysis.primary_style} • {agent_outputs.style_analysis.mood}
          </p>
        </div>
      )}

      {/* Products */}
      {agent_outputs?.product_recommendations && (
        <div className="bg-green-900/30 p-3 rounded border border-green-700">
          <h4 className="font-semibold text-green-300">🛋️ Products</h4>
          <p className="text-sm text-green-200">
            ${agent_outputs.product_recommendations.total_estimated_cost?.toFixed(2)}
          </p>
          <ul className="mt-1 space-y-1">
            {agent_outputs.product_recommendations.selected_products?.slice(0, 3).map((p, i) => (
              <li key={i} className="text-xs text-green-200">• {p.name}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Budget */}
      {agent_outputs?.budget_analysis && (
        <div className="bg-yellow-900/30 p-3 rounded border border-yellow-700">
          <h4 className="font-semibold text-yellow-300">💰 Budget</h4>
          <p className="text-sm text-yellow-200">
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