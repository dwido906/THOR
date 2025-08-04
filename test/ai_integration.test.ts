import { WebSocket } from 'ws';
import { fork, ChildProcess } from 'child_process';

function waitForService(serviceName: string, service: ChildProcess, readyMessage: string): Promise<void> {
  return new Promise((resolve, reject) => {
    service.stdout?.on('data', (data) => {
      const output = data.toString();
      console.log(`[${serviceName}]: ${output}`);
      if (output.includes(readyMessage)) {
        resolve();
      }
    });
    service.stderr?.on('data', (data) => {
      console.error(`[${serviceName} ERROR]: ${data.toString()}`);
    });
  });
}

describe('VRBLL Backend', () => {
  let aiService: ChildProcess;
  let vrbllService: ChildProcess;

  beforeAll(async () => {
    aiService = fork('index.ts', [], { cwd: '../ai', silent: true, execArgv: ['-r', 'ts-node/register'] });
    vrbllService = fork('ws_server.ts', [], { silent: true, execArgv: ['--loader', 'ts-node/esm'] });
    await Promise.all([
      waitForService('AI Service', aiService, 'Akira AI service running on port 4100'),
      waitForService('VRBLL Service', vrbllService, '[VRBLL] WebSocket server running on port 9001'),
    ]);
  }, 30000);

  afterAll(() => {
    aiService.kill();
    vrbllService.kill();
  });

  it('should receive a response from the AI service', (done) => {
    const ws = new WebSocket('ws://localhost:9001');
    ws.on('open', () => {
      ws.send(JSON.stringify({ type: 'auth', userId: 'test-user' }));
      ws.send(JSON.stringify({ type: 'msg', text: '/ai hello' }));
    });
    ws.on('message', (msg) => {
      const data = JSON.parse(msg.toString());
      if (data.userId === 'akira') {
        expect(data.text).toContain('Hello! I am Akira, your AI assistant.');
        done();
      }
    });
  }, 15000);
});
