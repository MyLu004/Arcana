// src/hooks/useChat.js
// COMPLETE VERSION: Budget + Animations + Image Upload + All UX
import { useState, useCallback } from 'react';
import { api } from '../services/api';

export function useChat() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: "Hello! I'm Arcana. Describe your dream space and I'll design it for you with AI-powered multi-agent orchestration.",
      timestamp: new Date()
    }
  ]);

  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  // Image handling
  const [uploadedImage, setUploadedImage] = useState(null);
  const [pendingFile, setPendingFile] = useState(null);
  const [pendingPreview, setPendingPreview] = useState(null);

  // NEW: File upload with preview
  const handleFileUpload = useCallback(async (file) => {
    if (!file) return;
    
    // Revoke previous preview
    if (pendingPreview) {
      try { URL.revokeObjectURL(pendingPreview); } catch(e) {}
    }
    
    const preview = URL.createObjectURL(file);
    setPendingFile(file);
    setPendingPreview(preview);
    
    // Show file queued message
    setMessages(prev => [...prev, {
      id: Date.now(),
      role: 'assistant',
      content: '📎 Image ready to upload with your next message',
      timestamp: new Date()
    }]);
  }, [pendingPreview]);

  // MERGED: Handles BOTH { text, budget, image } objects AND form events
  const handleSend = useCallback(async (eventOrData) => {
    // Determine if it's a data object or form event
    let messageData;
    
    if (eventOrData?.text !== undefined) {
      // Called with data object from ChatArea: { text, budget, image }
      messageData = {
        text: eventOrData.text,
        budget: eventOrData.budget,
        image: eventOrData.image
      };
    } else {
      // Called as form event (legacy support)
      if (eventOrData?.preventDefault) {
        eventOrData.preventDefault();
      }
      messageData = {
        text: input.trim(),
        budget: null,
        image: pendingPreview
      };
    }
    
    const { text, budget: userBudget } = messageData;
    
    if (!text.trim() || isLoading) return;
    
    console.log("Sending with budget:", userBudget);

    // Add user message
    const userMsgId = Date.now();
    const userMsg = {
      id: userMsgId,
      role: 'user',
      content: text,
      budget: userBudget, // Store budget for display
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMsg]);
    const currentInput = text;
    setInput('');
    setIsLoading(true);

    try {
      let controlImageUrl = null;
      
      // STEP 1: Upload image if present (with loading state)
      if (pendingFile) {
        try {
          // Show uploading message
          setMessages(prev => [...prev, {
            id: Date.now() + 1,
            role: 'assistant',
            content: '📤 Uploading your image...',
            isLoading: true,
            timestamp: new Date()
          }]);

          const uploadResult = await api.uploadImage(pendingFile);
          controlImageUrl = uploadResult.url;
          setUploadedImage(controlImageUrl);
          
          // Attach image URL to user's message
          setMessages(prev => prev.map(m => 
            m.id === userMsgId ? { ...m, image: controlImageUrl } : m
          ));
          
          // Remove uploading message
          setMessages(prev => prev.filter(m => !m.isLoading));
          
          // Clear pending
          if (pendingPreview) {
            try { URL.revokeObjectURL(pendingPreview); } catch(e) {}
          }
          setPendingFile(null);
          setPendingPreview(null);
          
        } catch (uploadErr) {
          console.error("Image upload error:", uploadErr);
          
          // Remove uploading message and show error
          setMessages(prev => [
            ...prev.filter(m => !m.isLoading),
            {
              id: Date.now() + 2,
              role: 'assistant',
              content: `Image upload failed: ${uploadErr.message}. Continuing without image...`,
              isError: true,
              timestamp: new Date()
            }
          ]);
        }
      }
      
      // STEP 2: Show "Generating" animation
      setMessages(prev => [...prev, {
        id: Date.now() + 3,
        role: 'assistant',
        content: 'Generating the request with the image right now',
        isLoading: true,
        timestamp: new Date()
      }]);

      // STEP 3: Call backend with budget
      const result = await api.generateDesign(
        currentInput,
        'living_room',
        'medium',
        userBudget, // ← Budget sent here!
        controlImageUrl
      );

      console.log("Design result:", result);

      // STEP 4: Remove loading message and show result
      setMessages(prev => [
        ...prev.filter(m => !m.isLoading), // Remove loading messages
        {
          id: Date.now() + 4,
          role: 'assistant',
          content: 'Your custom design is ready!',
          designData: result,
          timestamp: new Date()
        }
      ]);

    } catch (error) {
      console.error("Design generation error:", error);
      
      // Remove loading messages and show error
      setMessages(prev => [
        ...prev.filter(m => !m.isLoading),
        {
          id: Date.now() + 5,
          role: 'assistant',
          content: `Error: ${error.message}. Please try again.`,
          isError: true,
          timestamp: new Date()
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  }, [input, isLoading, pendingFile, pendingPreview]);

  const onNewChat = useCallback(() => {
    setMessages([{
      id: 1,
      role: 'assistant',
      content: "Hello! I'm Arcana. Describe your dream space and I'll design it for you with AI-powered multi-agent orchestration.",
      timestamp: new Date()
    }]);
    setInput('');
    setUploadedImage(null);
    clearPendingImage();
  }, []);

  const clearPendingImage = useCallback(() => {
    if (pendingPreview) {
      try { URL.revokeObjectURL(pendingPreview); } catch(e) {}
    }
    setPendingFile(null);
    setPendingPreview(null);
  }, [pendingPreview]);

  return {
    messages,
    input,
    setInput,
    isLoading,
    handleSend,
    handleFileUpload,
    onNewChat,
    uploadedImage,
    pendingImage: pendingPreview,
    clearPendingImage
  };
}