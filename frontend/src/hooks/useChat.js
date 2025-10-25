// src/hooks/useChat.js
import { useState, useCallback } from 'react';
import { api } from '../services/api';

export function useChat() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: '👋 Hello! I\'m Arcana. Describe your dream space and I\'ll design it for you with AI-powered multi-agent orchestration.',
      timestamp: new Date()
    }
  ]);
  
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedImage, setUploadedImage] = useState(null);

  const handleFileUpload = useCallback(async (file) => {
    try {
      setIsLoading(true);
      const result = await api.uploadImage(file);
      setUploadedImage(result.url);
      
      // Add confirmation message
      setMessages(prev => [...prev, {
        id: Date.now(),
        role: 'assistant',
        content: `✅ Image uploaded successfully! I'll use this as a reference for your design.`,
        timestamp: new Date()
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        id: Date.now(),
        role: 'assistant',
        content: `❌ Image upload failed: ${error.message}`,
        isError: true,
        timestamp: new Date()
      }]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const handleSend = useCallback(async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    // Add user message
    const userMsg = {
      id: Date.now(),
      role: 'user',
      content: input,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMsg]);
    const currentInput = input;
    setInput('');
    setIsLoading(true);

    try {
      // Call backend
      const result = await api.generateDesign(currentInput, {
        roomType: 'living_room',
        roomSize: 'medium',
        budget: 5000
      });

      // Add assistant response with design data
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        role: 'assistant',
        content: '✨ Your custom design is ready!',
        designData: result,
        timestamp: new Date()
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        role: 'assistant',
        content: `❌ Error: ${error.message}. Please try again.`,
        isError: true,
        timestamp: new Date()
      }]);
    } finally {
      setIsLoading(false);
    }
  }, [input, isLoading]);

  const onNewChat = useCallback(() => {
    setMessages([{
      id: 1,
      role: 'assistant',
      content: '🆕 New chat started! What space would you like to design?',
      timestamp: new Date()
    }]);
    setInput('');
    setUploadedImage(null);
  }, []);

  return {
    messages,
    input,
    setInput,
    isLoading,
    handleSend,
    handleFileUpload,
    onNewChat,
    uploadedImage
  };
}