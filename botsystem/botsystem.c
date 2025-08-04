// botsystem.c
// Minimal bot/plugin system implementation for VRBLL (C)
#include "botsystem_api.h"
#include <stdio.h>
#include <dlfcn.h>
#include <string.h>

#define MAX_PLUGINS 8
static void* plugin_handles[MAX_PLUGINS] = {0};
static char plugin_names[MAX_PLUGINS][64] = {{0}};

int botsystem_init(void) {
    memset(plugin_handles, 0, sizeof(plugin_handles));
    memset(plugin_names, 0, sizeof(plugin_names));
    return 0;
}

int botsystem_load_plugin(const char* path) {
    for (int i = 0; i < MAX_PLUGINS; ++i) {
        if (!plugin_handles[i]) {
            void* handle = dlopen(path, RTLD_LAZY);
            if (!handle) return -1;
            plugin_handles[i] = handle;
            strncpy(plugin_names[i], path, 63);
            return 0;
        }
    }
    return -1;
}

int botsystem_send_message(const char* plugin, const char* message) {
    for (int i = 0; i < MAX_PLUGINS; ++i) {
        if (plugin_handles[i] && strcmp(plugin_names[i], plugin) == 0) {
            void (*plugin_func)(const char*) = dlsym(plugin_handles[i], "plugin_entry");
            if (plugin_func) {
                plugin_func(message);
                return 0;
            }
        }
    }
    return -1;
}

int botsystem_unload_plugin(const char* plugin) {
    for (int i = 0; i < MAX_PLUGINS; ++i) {
        if (plugin_handles[i] && strcmp(plugin_names[i], plugin) == 0) {
            dlclose(plugin_handles[i]);
            plugin_handles[i] = NULL;
            plugin_names[i][0] = '\0';
            return 0;
        }
    }
    return -1;
}
