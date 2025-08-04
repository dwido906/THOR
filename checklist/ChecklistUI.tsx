// Minimal React UI for DayDreamers Checklist
import React, { useState } from 'react';
import { ChecklistItem } from './ChecklistItem';
import { addChecklistItem, getChecklist, updateChecklistItem } from './checklistApi';

export const ChecklistUI: React.FC = () => {
  const [title, setTitle] = useState('');
  const [desc, setDesc] = useState('');
  const [priority, setPriority] = useState<'low' | 'medium' | 'high'>('medium');
  const [items, setItems] = useState<ChecklistItem[]>(getChecklist());

  const handleAdd = () => {
    if (!title.trim()) return;
    const item = addChecklistItem({
      title,
      description: desc,
      priority,
      createdBy: 'currentUser',
    });
    setItems([...getChecklist()]);
    setTitle('');
    setDesc('');
  };

  const handleApprove = (id: string) => {
    updateChecklistItem(id, { status: 'approved' });
    setItems([...getChecklist()]);
  };

  return (
    <div>
      <h2>DayDreamers Checklist</h2>
      <input value={title} onChange={e => setTitle(e.target.value)} placeholder="Task title" />
      <input value={desc} onChange={e => setDesc(e.target.value)} placeholder="Description" />
      <select value={priority} onChange={e => setPriority(e.target.value as any)}>
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
      </select>
      <button onClick={handleAdd}>Add Task</button>
      <ul>
        {items.map(item => (
          <li key={item.id}>
            <b>{item.title}</b> ({item.priority}) - {item.status}
            <br />{item.description}
            {item.aiResult && <div><b>AI Result:</b> {item.aiResult}</div>}
            <button disabled={item.status !== 'awaiting-approval'} onClick={() => handleApprove(item.id)}>Approve</button>
          </li>
        ))}
      </ul>
    </div>
  );
};
