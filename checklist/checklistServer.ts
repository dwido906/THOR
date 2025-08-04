// Entrypoint for checklist API server
import express from 'express';
import checklistApi from './checklistApi';
import cors from 'cors';

const app = express();
app.use(cors());
app.use(express.json());
app.use('/api', checklistApi);

app.use((err: any, req: any, res: any, next: any) => {
  console.error(err);
  res.status(500).json({ error: 'Internal server error' });
});

const PORT = process.env.PORT || 4002;
app.listen(PORT, () => {
  console.log(`Checklist API running on port ${PORT}`);
});// Express backend API for DayDreamers Checklist
import express from 'express';
import bodyParser from 'body-parser';
import { ChecklistItem } from './ChecklistItem';
import { addChecklistItem, getChecklist, updateChecklistItem } from './checklistApi';

const app = express();
app.use(bodyParser.json());

// Get all checklist items
app.get('/api/checklist', (req, res) => {
  res.json(getChecklist());
});

// Add a new checklist item
app.post('/api/checklist', (req, res) => {
  const { title, description, priority, createdBy, assignedTo, deadline } = req.body;
  if (!title || !createdBy) return res.status(400).json({ error: 'Missing required fields' });
  const item = addChecklistItem({ title, description, priority, createdBy, assignedTo, deadline });
  res.json(item);
});

// Update a checklist item
app.patch('/api/checklist/:id', (req, res) => {
  const { id } = req.params;
  const updates = req.body;
  const updated = updateChecklistItem(id, updates);
  if (!updated) return res.status(404).json({ error: 'Not found' });
  res.json(updated);
});

// Health check
app.get('/api/checklist/health', (req, res) => res.send('ok'));

const PORT = process.env.CHECKLIST_PORT || 4000;
app.listen(PORT, () => console.log(`[Checklist] API running on :${PORT}`));
