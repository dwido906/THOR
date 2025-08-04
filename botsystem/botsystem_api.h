// botsystem_api.h
// Bot/plugin system API for VRBLL (C)
#ifndef BOTSYSTEM_API_H
#define BOTSYSTEM_API_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

// Initialize bot/plugin system
int botsystem_init(void);

// Load a plugin (C shared lib or Node.js script)
int botsystem_load_plugin(const char* path);

// Send message to plugin
int botsystem_send_message(const char* plugin, const char* message);

// Unload plugin
int botsystem_unload_plugin(const char* plugin);

#ifdef __cplusplus
}
#endif

#endif // BOTSYSTEM_API_H
