// Unit test for VRBLL message store
import { storeMessage, getMessages, ChatMessage } from '../messageStore';

describe('Message Store', () => {
  it('should store and retrieve messages', () => {
    const msg: ChatMessage = { id: 'm1', from: 'alice', content: 'hi', timestamp: Date.now() };
    storeMessage(msg);
    expect(getMessages()).toContainEqual(msg);
  });
});
