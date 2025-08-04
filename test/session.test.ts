// Unit test for VRBLL session management
import { createSession, getSession, removeSession, listSessions } from '../session';

describe('Session Management', () => {
  it('should create and retrieve a session', () => {
    const s = createSession('id1', 'alice');
    expect(getSession('id1')).toEqual(s);
  });
  it('should remove a session', () => {
    createSession('id2', 'bob');
    removeSession('id2');
    expect(getSession('id2')).toBeUndefined();
  });
  it('should list all sessions', () => {
    createSession('id3', 'carol');
    expect(listSessions().length).toBeGreaterThan(0);
  });
});
