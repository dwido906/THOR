wss.on('connection', (ws: WebSocket) => {
// VRBLL WebSocket Server
// Handles connections, messaging, and events

import { WebSocketServer, WebSocket } from 'ws';
import { createSession, removeSession, getSession, listSessions } from './session';
import { storeMessage, getMessages, ChatMessage } from './messageStore';
import { v4 as uuidv4 } from 'uuid';

// Simple in-memory rate limiter per session
const RATE_LIMIT_WINDOW = 5000; // ms
const RATE_LIMIT_MAX = 10; // max messages per window
const rateLimitMap = new Map<string, { count: number; last: number }>();

const wss = new WebSocketServer({ port: 8080 });

wss.on('connection', (ws: WebSocket) => {
  let sessionId: string | null = null;

  // Helper: broadcast to all clients
  function broadcast(data: any) {
    wss.clients.forEach(client => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(JSON.stringify(data));
      }
    });
  }

  // Helper: send chat history to a client
  function sendHistory() {
    ws.send(JSON.stringify({ type: 'history', messages: getMessages().slice(-50) }));
  }

  ws.on('message', (data) => {
    try {
      const msg = JSON.parse(data.toString());
      // Input validation
      if (!msg.type || typeof msg.type !== 'string') {
        ws.send(JSON.stringify({ type: 'error', error: 'Missing or invalid type' }));
        return;
      }
      if (msg.type === 'join') {
        if (sessionId) {
          ws.send(JSON.stringify({ type: 'error', error: 'Already joined' }));
          return;
        }
        if (!msg.username || typeof msg.username !== 'string' || msg.username.length < 2) {
          ws.send(JSON.stringify({ type: 'error', error: 'Invalid username' }));
          return;
        }
        sessionId = uuidv4();
        createSession(sessionId, msg.username);
        ws.send(JSON.stringify({ type: 'welcome', sessionId }));
        // Notify all of presence
        broadcast({ type: 'presence', event: 'join', username: msg.username });
        sendHistory();
      } else if (msg.type === 'message' && sessionId) {
        // Rate limiting
        const now = Date.now();
        const rl = rateLimitMap.get(sessionId) || { count: 0, last: now };
        if (now - rl.last > RATE_LIMIT_WINDOW) {
          rl.count = 0;
          rl.last = now;
        }
        rl.count++;
        rateLimitMap.set(sessionId, rl);
        if (rl.count > RATE_LIMIT_MAX) {
          ws.send(JSON.stringify({ type: 'error', error: 'Rate limit exceeded' }));
          return;
        }
        if (!msg.content || typeof msg.content !== 'string' || msg.content.length === 0) {
          ws.send(JSON.stringify({ type: 'error', error: 'Empty message' }));
          return;
        }
        const user = getSession(sessionId)?.username || 'unknown';
        const chatMsg: ChatMessage = {
          id: uuidv4(),
          from: user,
          content: msg.content,
          timestamp: now
        };
        storeMessage(chatMsg);
        broadcast({ type: 'message', ...chatMsg });
      } else {
        ws.send(JSON.stringify({ type: 'error', error: 'Unknown or unauthorized event' }));
      }
    } catch (e) {
      ws.send(JSON.stringify({ type: 'error', error: 'Invalid message format' }));
    }
  });

  ws.on('close', () => {
    if (sessionId) {
      const user = getSession(sessionId)?.username;
      removeSession(sessionId);
      if (user) broadcast({ type: 'presence', event: 'leave', username: user });
    }
  });
});

console.log('[VRBLL] WebSocket server running on :8080');
