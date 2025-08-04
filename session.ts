// VRBLL Session Management
// Handles user sessions for chat backend

export interface Session {
  id: string;
  username: string;
  connectedAt: number;
}

const sessions = new Map<string, Session>();

export function createSession(id: string, username: string): Session {
  const session = { id, username, connectedAt: Date.now() };
  sessions.set(id, session);
  return session;
}

export function getSession(id: string): Session | undefined {
  return sessions.get(id);
}

export function removeSession(id: string): void {
  sessions.delete(id);
}

export function listSessions(): Session[] {
  return Array.from(sessions.values());
}
