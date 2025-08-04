// meshsync_api.h
// Mesh-native sync API for VRBLL (C)
#ifndef MESHSYNC_API_H
#define MESHSYNC_API_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

// Initialize mesh sync
int meshsync_init(const char* node_id);

// Discover peers
int meshsync_discover_peers(void);

// Sync message/state with peers
int meshsync_sync_data(const void* data, size_t size);

// Handle incoming sync
int meshsync_handle_incoming(const void* data, size_t size);

#ifdef __cplusplus
}
#endif

#endif // MESHSYNC_API_H
