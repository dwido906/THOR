// test_collabApi.ts
// Test stub for VRBLL collaboration TypeScript API
import { initCollab, createDoc, editDoc, getDoc } from './collabApi';

describe('collabApi', () => {
  it('should initialize collab', async () => {
    await initCollab();
  });
  it('should create, edit, and get doc', async () => {
    await createDoc('doc1');
    await editDoc('doc1', 'alice', 'Hello, world!');
    const content = await getDoc('doc1');
    expect(typeof content).toBe('string');
  });
});
