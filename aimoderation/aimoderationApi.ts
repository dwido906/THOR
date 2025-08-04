// aimoderationApi.ts
// TypeScript API for AI-powered moderation in VRBLL

import * as store from './aimoderationStore';

export function initAIModeration(): Promise<void> {
  return store.initAIModeration();
}

export function moderateMessage(user: string, message: string): Promise<{ flagged: boolean; reason?: string }> {
  return store.moderateMessage(user, message);
}

export function moderateVoice(data: ArrayBuffer): Promise<{ flagged: boolean; reason?: string }> {
  return store.moderateVoice(data);
}
