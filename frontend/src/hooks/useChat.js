// src/hooks/useChat.js
import { useState, useCallback } from 'react';
import { api } from '../services/api';

export function useChat() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: 'Hello! I\'m Arcana. Describe your dream space and I\'ll design it for you with AI-powered multi-agent orchestration.',
      timestamp: new Date()
    }
  ]);
  
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  // uploadedImage is the URL returned from the server after actual upload
  const [uploadedImage, setUploadedImage] = useState(null);
  // pendingFile is a File object chosen by the user but not yet uploaded
  const [pendingFile, setPendingFile] = useState(null);
  const [pendingPreview, setPendingPreview] = useState(null);

  const handleFileUpload = useCallback(async (file) => {
    // Stage the file locally and show a preview. Actual upload will happen on Send.
    if (!file) return;
    // revoke previous preview if any
    if (pendingPreview) {
      try { URL.revokeObjectURL(pendingPreview); } catch(e) {}
    }
    const preview = URL.createObjectURL(file);
    setPendingFile(file);
    setPendingPreview(preview);
    // Add a small assistant note that the file is queued
    setMessages(prev => [...prev, {
      id: Date.now(),
      role: 'assistant',
      content: null,
      timestamp: new Date()
    }]);
  }, [pendingPreview]);

  const handleSend = useCallback(async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    // Add user message (capture id so we can attach image URL after upload)
    const userMsgId = Date.now();
    const userMsg = {
      id: userMsgId,
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMsg]);
    const currentInput = input;
    setInput('');
    setIsLoading(true);

    try {
      let controlImageUrl = null;
      // If user selected a file previously, upload it now and get the public URL
      if (pendingFile) {
        try {
          setIsLoading(true);
          const uploadResult = await api.uploadImage(pendingFile);
          controlImageUrl = uploadResult.url;
          setUploadedImage(controlImageUrl);
          // Attach the uploaded image URL to the user's message so it's visible in the chat
          setMessages(prev => prev.map(m => m.id === userMsgId ? { ...m, image: controlImageUrl } : m));
          // clear pending preview
          if (pendingPreview) {
            try { URL.revokeObjectURL(pendingPreview); } catch(e) {}
          }
          setPendingFile(null);
          setPendingPreview(null);
          // add confirmation message
          setMessages(prev => [...prev, {
            id: Date.now() + 2,
            role: 'assistant',
            content: `Generating the request with the image right now`,
            timestamp: new Date()
          }]);
        } catch (uploadErr) {
          setMessages(prev => [...prev, {
            id: Date.now() + 2,
            role: 'assistant',
            content: `❌ Image upload failed: ${uploadErr.message}. Sending request without image.`,
            isError: true,
            timestamp: new Date()
          }]);
        } finally {
          setIsLoading(false);
        }
      }
      // Call backend
      const result = await api.generateDesign(currentInput, 'living_room', 'medium', 5000, controlImageUrl);

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
  }, [input, isLoading, pendingFile, pendingPreview]);

  const onNewChat = useCallback(() => {
    setMessages([{
      id: 1,
      role: 'assistant',
      content: 'Hello! I\'m Arcana. Describe your dream space and I\'ll design it for you with AI-powered multi-agent orchestration.',
      timestamp: new Date()
    }]);
    setInput('');
    setUploadedImage(null);
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