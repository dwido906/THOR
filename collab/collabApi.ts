// collabApi.ts
// TypeScript API for collaboration tools in VRBLL

import * as store from './collabStore';

export function initCollab(): Promise<void> {
  return store.initCollab();
}

export function createDoc(docId: string): Promise<void> {
  return store.createDoc(docId);
}

export function editDoc(docId: string, user: string, content: string): Promise<void> {
  return store.editDoc(docId, user, content);
}

export function getDoc(docId: string): Promise<string> {
  return store.getDoc(docId);
}
