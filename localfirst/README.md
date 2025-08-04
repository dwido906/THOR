# VRBLL Local-First Architecture

This module provides local-first data storage, offline support, and conflict resolution for VRBLL chat, voice, and collaboration features. It is designed for modular integration with the Akira OS mesh and sync APIs.

## Features
- Local persistent storage for messages, files, and state
- Offline-first operation with automatic sync when online
- Conflict resolution strategies (CRDT, last-writer-wins, etc.)
- Integration points for mesh-native sync and E2E encryption
- Testable, containerized, and modular

## Integration
- Exposes C and TypeScript APIs for VRBLL core and UI
- Works with Akira mesh and GateScore authentication

## Development
- See `localfirst_api.h` and `localfirstApi.ts` for API details
- Run `test_localfirst.c` and `test_localfirstApi.ts` for test stubs

---
