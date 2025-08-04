// Modular checklist API for VRBLL
import express from 'express';
import { ChecklistTask, ChecklistStatus } from './ChecklistTask';
import { authenticateJWT, requireRole, AuthUser } from './auth';
import { v4 as uuidv4 } from 'uuid';
import fs from 'fs';
import path from 'path';

const DATA_FILE = path.join(__dirname, 'checklist_tasks.json');
function load(): ChecklistTask[] {
  if (!fs.existsSync(DATA_FILE)) return [];
  return JSON.parse(fs.readFileSync(DATA_FILE, 'utf-8'));
}
function save(tasks: ChecklistTask[]) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(tasks, null, 2));
}
let tasks: ChecklistTask[] = load();

const router = express.Router();

// Create new task
router.post('/tasks', authenticateJWT, requireRole('member'), (req, res) => {
  const { description, priority, assignedUser } = req.body;
  if (!description || !priority || !assignedUser) return res.status(400).json({ error: 'Missing fields' });
  const task: ChecklistTask = {
    id: uuidv4(),
    description,
    priority,
    status: 'pending',
    assignedUser,
    createdAt: Date.now(),
    updatedAt: Date.now(),
  };
  tasks.push(task);
  save(tasks);
  res.status(201).json(task);
});

// List all tasks
router.get('/tasks', authenticateJWT, (req, res) => {
  res.json(tasks);
});

// Get task details
router.get('/tasks/:id', authenticateJWT, (req, res) => {
  const task = tasks.find(t => t.id === req.params.id);
  if (!task) return res.status(404).json({ error: 'Not found' });
  res.json(task);
});

// Update task status
router.patch('/tasks/:id/status', authenticateJWT, (req, res) => {
  const { status } = req.body;
  const task = tasks.find(t => t.id === req.params.id);
  if (!task) return res.status(404).json({ error: 'Not found' });
  if (!['pending','processing','done','approved'].includes(status)) return res.status(400).json({ error: 'Invalid status' });
  task.status = status as ChecklistStatus;
  task.updatedAt = Date.now();
  save(tasks);
  res.json(task);
});

// Submit AI-generated result (member or reviewer)
router.post('/tasks/:id/ai-result', authenticateJWT, (req, res) => {
  const { aiResult } = req.body;
  const task = tasks.find(t => t.id === req.params.id);
  if (!task) return res.status(404).json({ error: 'Not found' });
  task.aiResult = aiResult;
  task.updatedAt = Date.now();
  save(tasks);
  res.json(task);
});

// Approve task (reviewer only)
router.post('/tasks/:id/approve', authenticateJWT, requireRole('reviewer'), (req, res) => {
  const task = tasks.find(t => t.id === req.params.id);
  if (!task) return res.status(404).json({ error: 'Not found' });
  task.status = 'approved';
  task.updatedAt = Date.now();
  save(tasks);
  res.json(task);
});

export default router;// Minimal backend API for checklist management
import { ChecklistItem } from './ChecklistItem';
import { v4 as uuidv4 } from 'uuid';

const checklist: ChecklistItem[] = [];

export function addChecklistItem(item: Omit<ChecklistItem, 'id' | 'createdAt' | 'updatedAt'>): ChecklistItem {
  const newItem: ChecklistItem = {
    ...item,
    id: uuidv4(),
    createdAt: Date.now(),
    updatedAt: Date.now(),
    status: 'pending',
  };
  checklist.push(newItem);
  return newItem;
}

export function getChecklist(): ChecklistItem[] {
  return checklist;
}

export function updateChecklistItem(id: string, updates: Partial<ChecklistItem>): ChecklistItem | undefined {
  const item = checklist.find(i => i.id === id);
  if (item) {
    Object.assign(item, updates, { updatedAt: Date.now() });
    return item;
  }
  return undefined;
}
