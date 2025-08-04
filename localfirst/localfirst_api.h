// localfirst_api.h
// Local-first storage and sync API for VRBLL (C)
#ifndef LOCALFIRST_API_H
#define LOCALFIRST_API_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

// Initialize local storage
int localfirst_init(const char* db_path);

// Store a message locally
int localfirst_store_message(const char* channel, const char* user, const char* message, uint64_t timestamp);

// Retrieve messages (returns count, fills buffer)
int localfirst_get_messages(const char* channel, char* buffer, size_t bufsize);

// Sync with mesh/remote peers
int localfirst_sync(void);

// Resolve conflicts
int localfirst_resolve_conflicts(void);

#ifdef __cplusplus
}
#endif

#endif // LOCALFIRST_API_H
