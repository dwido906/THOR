// e2ecryptoApi.ts
// TypeScript API for end-to-end encryption in VRBLL

import * as store from './e2ecryptoStore';

export function initE2ECrypto(): Promise<void> {
  return store.initE2ECrypto();
}

export function generateKeys(): Promise<{ pubkey: string; privkey: string }> {
  return store.generateKeys();
}

export function encryptMessage(plaintext: string, pubkey: string): Promise<string> {
  return store.encryptMessage(plaintext, pubkey);
}

export function decryptMessage(ciphertext: string, privkey: string): Promise<string> {
  return store.decryptMessage(ciphertext, privkey);
}
