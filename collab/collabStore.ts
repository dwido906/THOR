// collabStore.ts
// Minimal collaboration tools implementation for VRBLL (TypeScript)
import * as fs from 'fs';

const DB_FILE = 'vrbll_docs.json';

let docs: Record<string, string[]> = {};

function loadDocs() {
  if (fs.existsSync(DB_FILE)) {
    docs = JSON.parse(fs.readFileSync(DB_FILE, 'utf-8'));
  } else {
    docs = {};
  }
}

function saveDocs() {
  fs.writeFileSync(DB_FILE, JSON.stringify(docs, null, 2));
}

export async function initCollab() {
  loadDocs();
}

export async function createDoc(docId: string) {
  if (!docs[docId]) docs[docId] = [];
  saveDocs();
}

export async function editDoc(docId: string, user: string, content: string) {
  if (!docs[docId]) docs[docId] = [];
  docs[docId].push(`${user}: ${content}`);
  saveDocs();
}

export async function getDoc(docId: string): Promise<string> {
  loadDocs();
  return (docs[docId] || []).join('\n');
}
