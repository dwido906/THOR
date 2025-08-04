import express from 'express';
import http from 'http';
import cors from 'cors';
import { WebSocketServer } from 'ws';
import axios from 'axios';

const app = express();
app.use(cors());

const server = http.createServer(app);
const wss = new WebSocketServer({ server });
const users: Record<string, any> = {};

wss.on('connection', (ws, req) => {
  let userId: string;
  ws.on('message', async (msg) => {
    try {
      const data = JSON.parse(msg.toString());
      if (data.type === 'auth') {
        // Simplified auth for standalone app
        users[data.userId] = ws;
        userId = data.userId;
        ws.send(JSON.stringify({ type: 'auth', status: 'success' }));
      } else if (data.type === 'msg') {
        if (data.text.startsWith('/ai')) {
          // Command for AI
          const command = data.text.substring(4).trim();
          const res = await axios.post('http://localhost:4100/api/ai/event', {
            command,
            user: { id: userId },
          });
          ws.send(JSON.stringify({ type: 'msg', text: `Akira: ${JSON.stringify(res.data)}`, userId: 'akira' }));
        } else {
          // Broadcast to all
          Object.values(users).forEach((u: any) => u.send(JSON.stringify(data)));
        }
      }
    } catch (e) {
      ws.send(JSON.stringify({ type: 'error', error: 'Malformed message' }));
    }
  });
});

const PORT = process.env.VRBLL_PORT || 9001;
server.listen(PORT, () => {
  console.log(`[VRBLL] WebSocket server running on port ${PORT}`);
});

