// vrbll chat backend entry
import http from 'http';
import WebSocket, { WebSocketServer } from 'ws';

const server = http.createServer();
const wss = new WebSocketServer({ server });

wss.on('connection', ws => {
  ws.on('message', message => {
    ws.send(`echo: ${message}`);
  });
});

server.listen(8080, () => {
  console.log('vrbll chat backend running on :8080');
});
