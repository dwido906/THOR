// Add Node.js types for process
/// <reference types="node" />
// Persistent checklist store using JSON file

// Use CommonJS imports for Node.js compatibility
import { ChecklistItem } from './ChecklistItem';
// @ts-ignore
const fs = require('fs');
// @ts-ignore
const path = require('path');


// __dirname workaround for TypeScript/Node.js
const _dirname = (typeof globalThis !== 'undefined' && (globalThis as any).__dirname) ? (globalThis as any).__dirname : (typeof process !== 'undefined' ? process.cwd() : '.');
const DATA_FILE = path.join(_dirname, 'checklist.json');

function load(): ChecklistItem[] {
  if (!fs.existsSync(DATA_FILE)) return [];
  return JSON.parse(fs.readFileSync(DATA_FILE, 'utf-8'));
}

function save(items: ChecklistItem[]) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(items, null, 2));
}

let checklist: ChecklistItem[] = load();

export function getChecklist(): ChecklistItem[] {
  return checklist;
}

export function addChecklistItem(item: Omit<ChecklistItem, 'id' | 'createdAt' | 'updatedAt'>): ChecklistItem {
  const newItem: ChecklistItem = {
    ...item,
    id: (Date.now() + Math.random()).toString(36),
    createdAt: Date.now(),
    updatedAt: Date.now(),
    status: 'pending',
  };
  checklist.push(newItem);
  save(checklist);
  return newItem;
}

export function updateChecklistItem(id: string, updates: Partial<ChecklistItem>): ChecklistItem | undefined {
  const item = checklist.find(i => i.id === id);
  if (item) {
    Object.assign(item, updates, { updatedAt: Date.now() });
    save(checklist);
    return item;
  }
  return undefined;
}
