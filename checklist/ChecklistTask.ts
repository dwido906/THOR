// Checklist task schema for VRBLL
export type ChecklistStatus = 'pending' | 'processing' | 'done' | 'approved';

export interface ChecklistTask {
  id: string;
  description: string;
  priority: 'low' | 'medium' | 'high';
  status: ChecklistStatus;
  assignedUser: string;
  createdAt: number;
  updatedAt: number;
  aiResult?: string;
}
