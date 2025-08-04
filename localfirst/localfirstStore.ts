// localfirstStore.ts
// Minimal local-first storage implementation for VRBLL (TypeScript)
import * as fs from 'fs';

const DB_FILE = 'vrbll_local.json';

let db: Record<string, any[]> = {};

function loadDB() {
  if (fs.existsSync(DB_FILE)) {
    db = JSON.parse(fs.readFileSync(DB_FILE, 'utf-8'));
  } else {
    db = {};
  }
}

function saveDB() {
  fs.writeFileSync(DB_FILE, JSON.stringify(db, null, 2));
}

export async function initLocalStorage(dbPath?: string) {
  loadDB();
}

export async function storeMessage(channel: string, user: string, message: string, timestamp: number) {
  if (!db[channel]) db[channel] = [];
  db[channel].push({ user, message, timestamp });
  saveDB();
}

export async function getMessages(channel: string): Promise<string[]> {
  loadDB();
  return (db[channel] || []).map(m => `${channel}|${m.user}|${m.message}|${m.timestamp}`);
}

export async function syncWithMesh() {
  // Stub: mesh/remote sync not implemented
}

export async function resolveConflicts() {
  // Stub: conflict resolution not implemented
}
