// test_e2ecryptoApi.ts
// Test stub for VRBLL E2E crypto TypeScript API
import { initE2ECrypto, generateKeys, encryptMessage, decryptMessage } from './e2ecryptoApi';

describe('e2ecryptoApi', () => {
  it('should initialize E2E crypto', async () => {
    await initE2ECrypto();
  });
  it('should generate keys', async () => {
    const keys = await generateKeys();
    expect(keys).toHaveProperty('pubkey');
    expect(keys).toHaveProperty('privkey');
  });
  it('should encrypt and decrypt messages', async () => {
    const keys = await generateKeys();
    const ciphertext = await encryptMessage('secret', keys.pubkey);
    await decryptMessage(ciphertext, keys.privkey);
  });
});
