
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Drawer, List, ListItem, ListItemText, Button, Typography } from '@mui/material';

export default function App() {
  const [chats, setChats] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetch("http://localhost:8000/chat/")
      .then(res => res.json())
      .then(data => setChats(data))
      .catch(err => console.error(err));
  }, []);

  const handleStartChat = () => {
    navigate("/chat");
  };

  return (
    <Box sx={{ display: 'flex', height: '100vh' }}>
      <Drawer
        variant="permanent"
        sx={{
          width: 240,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: { width: 240, boxSizing: 'border-box' },
        }}
      >
        <Typography variant="h6" sx={{ padding: 2 }}>
          Chats
        </Typography>
        <List>
          {chats.length > 0 ? chats.map((chat, idx) => (
            <ListItem button key={idx}>
              <ListItemText primary={chat.chat_id} />
            </ListItem>
          )) : <ListItem><ListItemText primary="No chats yet" /></ListItem>}
        </List>
      </Drawer>

      <Box component="main" sx={{ flexGrow: 1, p: 3, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <Button variant="contained" onClick={handleStartChat}>
          Start Chat
        </Button>
      </Box>
    </Box>
  );
}
