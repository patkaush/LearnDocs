
import React, { useState } from 'react';
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
  TypingIndicator
} from '@chatscope/chat-ui-kit-react';
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
import { useParams } from 'react-router-dom';
import StudyMode from './StudyMode';
import {
  Box,
  Drawer,
  List,
  ListItem,
  ListItemText,
  Toolbar,
  Typography,
  Divider
} from '@mui/material';

const drawerWidth = 240;

const ChatWindow = () => {
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [uploading, setUploading] = useState(false);

  const { chatId } = useParams();

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setUploading(true);

    const formData = new FormData();
    formData.append("file", file);

    fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: formData,
    }).then(async (res) => {
        if (!res.ok) {
          const errorData = await res.json();
          throw new Error(errorData.detail || "Upload failed");
        }
        return res.json();
      })
      .then((data) => {
        setUploadedFiles((prev) => [...prev, data.filename]);
      })
      .catch((err) => {
        console.error("Upload failed:", err);
      }).finally(() => {
        setUploading(false);
      });
  };

  const handleSend = async (innerHtml) => {
    if (!innerHtml.trim()) return;

    const userMessage = {
      message: innerHtml,
      direction: 'outgoing',
      sender: 'user',
    };

    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: innerHtml }),
      });

      const data = await response.json();

      await new Promise(res => setTimeout(res, 600));

      const botMessage = {
        message: data,
        direction: 'incoming',
        sender: 'bot',
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('API error:', error);
    }

    setIsTyping(false);
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: 'auto', padding: 2 }}>
          <Typography variant="h6">Chat App</Typography>
          <Divider sx={{ my: 2 }} />
          <List>
            <ListItem><ListItemText primary={`Chat ID: ${chatId}`} /></ListItem>
          </List>
        </Box>
      </Drawer>

      <Box component="main" sx={{ flexGrow: 1, p: 3, marginLeft: `${drawerWidth}px`, width: `calc(100% - ${drawerWidth}px)` }}>
        <Box sx={{ height: 'calc(100vh - 64px)', display: 'flex', background: '#f0f2f5' }}>
          <Box sx={{ flex: 2, padding: '20px' }}>
            <MainContainer>
              <ChatContainer>
                <MessageList typingIndicator={isTyping && <TypingIndicator content="Bot is typing" />}>
                  {messages.map((msg, idx) => (
                    <Message
                      key={idx}
                      model={{
                        message: msg.message,
                        sentTime: 'just now',
                        direction: msg.direction,
                        position: 'single',
                      }}
                    />
                  ))}
                </MessageList>
                <MessageInput placeholder="Type your message..." onSend={handleSend} attachButton={false} />
              </ChatContainer>
            </MainContainer>
          </Box>

          <Box sx={{ flex: 1, padding: '20px', background: '#fff' }}>
            <h3>Upload File</h3>
            <input
              type="file"
              onChange={handleFileUpload}
              style={{
                marginBottom: '20px',
                padding: '6px',
                border: '1px solid #ccc',
                borderRadius: '4px',
              }}
            />

            {uploading ? (
              <Box sx={{ marginTop: '20px' }}>
                <p>⏳ Processing document...</p>
              </Box>
            ) : (
              <>
                <h3>📄 Uploaded Files</h3>
                {uploadedFiles.length === 0 ? (
                  <p>No files uploaded yet.</p>
                ) : (
                  <ul style={{ paddingLeft: 20 }}>
                    {uploadedFiles.map((file, idx) => (
                      <li key={idx}>{file}</li>
                    ))}
                  </ul>
                )}
              </>
            )}
            <Box sx={{ mt: 4 }}>
              <StudyMode />
            </Box>
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default ChatWindow;
