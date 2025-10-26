import { useRef, useEffect, useState } from "react";
import FileUpload from "./FileUpload";
import BeforeAfterSlider from "./BeforeAfterSlider";
import ProductGallery from "./ProductGallery";
import CostBreakdown from "./CostBreakdown";

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
  const [budget, setBudget] = useState("")

  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);


  const onSubmit = (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    handleSend({
      text: input,
      budget: budget === "" ? null : Number(budget), // send a number or null
      image: pendingImage || null,
    });}

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
              className={`max-w-[100%] rounded-lg px-4 py-3 ${
                message.role === 'user'
                  ? 'bg-[var(--color-secondary)] text-black'
                  : message.isError
                  ? 'bg-red-100 text-red-800 border border-red-300'
                  : 'bg-[var(--color-button)] text-white font-semi-bold'
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{message.content}</p>

              {/* User uploaded image */}
              {message.image && (
                <div className="mt-2">
                  <img 
                    src={message.image} 
                    alt="user-upload" 
                    className="max-w-xs rounded shadow-md" 
                  />
                </div>
              )}

              {/*  NEW: Complete Design Results with Visuals */}
              {message.designData && (
                <DesignResults data={message.designData} />
              )}
            </div>
          </div>
        ))}

        {/* Animated assistant 'typing' bubble while generating */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="max-w-[60%] rounded-lg px-4 py-3 bg-[var(--color-button)] text-white">
              <div className="flex items-center gap-3">
                <div className="flex items-center gap-1">
                  <span className="inline-block h-2 w-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '0s' }} />
                  <span className="inline-block h-2 w-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                  <span className="inline-block h-2 w-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
                <span className="text-sm">Generating response...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Preview of pending image */}
      {pendingImage && (
        <div className="p-2">
          <div className="flex items-center space-x-3 p-2 rounded">
            <img 
              src={pendingImage} 
              alt="preview" 
              className="h-20 w-28 object-cover rounded" 
            />
            {/* <span className="text-sm text-white">Ready to upload</span> */}
          </div>
        </div>
      )}

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

        <input
          type="number"
          min="0"
          step="1"
          placeholder="Budget ($)"
          value={budget}
          onChange={(e) => setBudget(e.target.value)}
          disabled={isLoading}
          className="w-40 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-black disabled:bg-gray-200"
          aria-label="Budget in USD"
        />
        
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          className="bg-[var(--color-secondary)] text-black px-4 py-2 rounded-lg hover:bg-[var(--color-button)] hover:text-white disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? '...' : 'Send'}
        </button>

        <FileUpload onFileUpload={handleFileUpload} />

      </form>
      
    </div>
  );
}

//  ENHANCED: Component to display complete design results
function DesignResults({ data }) {
  const { agent_outputs, confidence_scores, room_images } = data;

  // Extract data
  const styleData = agent_outputs?.style_analysis || {};
  const productData = agent_outputs?.product_recommendations || {};
  const budgetData = agent_outputs?.budget_analysis || {};
  const products = productData?.selected_products || [];

  return (
    <div className="mt-4 space-y-4 w-full">
      
      {/* NEW: Before/After Room Transformation */}
      {room_images?.original && room_images?.transformed && (
        <BeforeAfterSlider
          beforeImage={room_images.original}
          afterImage={room_images.transformed}
        />
      )}

      {/* Style Summary Card */}
      {styleData.primary_style && (
        <div className="bg-white p-4 rounded-lg shadow-md">
          <h3 className="font-bold text-lg text-gray-800 mb-2">
             Design Style
          </h3>
          <div className="flex flex-wrap gap-2">
            <span className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-semibold">
              {styleData.primary_style}
            </span>
            {styleData.mood && (
              <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                {styleData.mood}
              </span>
            )}
            {styleData.color_palette?.map((color, i) => (
              <span 
                key={i}
                className="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-sm"
              >
                {color}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* NEW: Visual Product Gallery */}
      {products.length > 0 && (
        <ProductGallery products={products} />
      )}

      {/*  NEW: Cost Breakdown */}
      {(budgetData || productData) && (
        <CostBreakdown 
          budgetData={budgetData} 
          productData={productData} 
        />
      )}

      {/* Agent Confidence Scores */}
      {confidence_scores && Object.keys(confidence_scores).length > 0 && (
        <div className="bg-white p-4 rounded-lg shadow-md">
          <h3 className="font-bold text-gray-800 mb-3">AI Confidence</h3>
          <div className="space-y-2">
            {Object.entries(confidence_scores).map(([agent, score]) => (
              <div key={agent} className="flex items-center gap-2">
                <span className="text-sm text-gray-600 w-32 capitalize">
                  {agent.replace('_', ' ')}
                </span>
                <div className="flex-1 bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-green-500 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${score * 100}%` }}
                  />
                </div>
                <span className="text-sm font-semibold text-gray-700 w-12 text-right">
                  {(score * 100).toFixed(0)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default ChatArea;