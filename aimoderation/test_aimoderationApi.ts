// test_aimoderationApi.ts
// Test stub for VRBLL AI moderation TypeScript API
import { initAIModeration, moderateMessage, moderateVoice } from './aimoderationApi';

describe('aimoderationApi', () => {
  it('should initialize AI moderation', async () => {
    await initAIModeration();
  });
  it('should moderate messages', async () => {
    const result = await moderateMessage('alice', 'test message');
    expect(result).toHaveProperty('flagged');
  });
  it('should moderate voice', async () => {
    const result = await moderateVoice(new ArrayBuffer(8));
    expect(result).toHaveProperty('flagged');
  });
});
