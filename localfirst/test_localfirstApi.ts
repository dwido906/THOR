// test_localfirstApi.ts
// Test stub for VRBLL local-first TypeScript API
import { initLocalStorage, storeMessage, getMessages, syncWithMesh, resolveConflicts } from './localfirstApi';

describe('localfirstApi', () => {
  it('should initialize local storage', async () => {
    await initLocalStorage('testdb.vrbll');
  });
  it('should store and retrieve messages', async () => {
    await storeMessage('general', 'alice', 'Hello, world!', 1234567890);
    const msgs = await getMessages('general');
    expect(Array.isArray(msgs)).toBe(true);
  });
  it('should sync and resolve conflicts', async () => {
    await syncWithMesh();
    await resolveConflicts();
  });
});
