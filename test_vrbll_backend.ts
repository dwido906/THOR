import { WebSocket } from 'ws';
describe('VRBLL WebSocket', () => {
  it('authenticates and broadcasts messages', (done) => {
    const ws = new WebSocket('ws://localhost:9001');
    ws.on('open', () => {
      ws.send(JSON.stringify({ type: 'auth', userId: 'u1' }));
    });
    ws.on('message', (msg) => {
      const data = JSON.parse(msg.toString());
      if (data.type === 'auth') {
        expect(typeof data.score).toBe('number');
        ws.send(JSON.stringify({ type: 'msg', text: 'hello' }));
      } else if (data.type === 'msg') {
        expect(data.text).toBe('hello');
        ws.close();
        done();
      }
    });
  });
});
