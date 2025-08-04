// e2ecryptoStore.ts
// Minimal E2E crypto implementation for VRBLL (TypeScript)
import * as crypto from 'crypto';

export async function initE2ECrypto() {
  // No-op for Node.js
}

export async function generateKeys() {
  const { publicKey, privateKey } = crypto.generateKeyPairSync('ed25519');
  return {
    pubkey: publicKey.export({ type: 'spki', format: 'pem' }).toString(),
    privkey: privateKey.export({ type: 'pkcs8', format: 'pem' }).toString(),
  };
}

export async function encryptMessage(plaintext: string, pubkey: string) {
  // For demo: just base64 encode (real E2E would use libsodium or WebCrypto)
  return Buffer.from(plaintext).toString('base64');
}

export async function decryptMessage(ciphertext: string, privkey: string) {
  // For demo: just base64 decode
  return Buffer.from(ciphertext, 'base64').toString('utf-8');
}
