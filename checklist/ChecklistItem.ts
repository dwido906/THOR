// Checklist item type for DayDreamers system
export interface ChecklistItem {
  id: string;
  title: string;
  description: string;
  status: 'pending' | 'in-progress' | 'ai-review' | 'awaiting-approval' | 'approved' | 'rejected';
  priority: 'low' | 'medium' | 'high';
  createdBy: string;
  assignedTo?: string;
  deadline?: string;
  createdAt: number;
  updatedAt: number;
  aiResult?: string;
  aiArtifacts?: string[];
  feedback?: string;
}
