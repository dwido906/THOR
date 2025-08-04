# VRBLL End-to-End Encryption (E2E)

This module provides secure, end-to-end encrypted messaging and voice for VRBLL. It handles key management, encryption/decryption, and secure session establishment, integrating with local-first and mesh sync modules.

## Features
- E2E encryption for messages and voice
- Key generation, storage, and rotation
- Secure session establishment and teardown
- Integration with mesh sync and local-first modules
- Modular, containerized, and testable

## Integration
- C and TypeScript APIs for VRBLL core and UI
- Works with Akira mesh and GateScore authentication

## Development
- See `e2ecrypto_api.h` and `e2ecryptoApi.ts` for API details
- Run `test_e2ecrypto.c` and `test_e2ecryptoApi.ts` for test stubs

---
