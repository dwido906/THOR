// localfirstApi.ts
// TypeScript API for local-first storage and sync in VRBLL

import * as store from './localfirstStore';

export function initLocalStorage(dbPath?: string): Promise<void> {
  return store.initLocalStorage(dbPath);
}

export function storeMessage(channel: string, user: string, message: string, timestamp: number): Promise<void> {
  return store.storeMessage(channel, user, message, timestamp);
}

export function getMessages(channel: string): Promise<string[]> {
  return store.getMessages(channel);
}

export function syncWithMesh(): Promise<void> {
  return store.syncWithMesh();
}

export function resolveConflicts(): Promise<void> {
  return store.resolveConflicts();
}
