// test_botsystem.c
// Test stub for VRBLL bot/plugin system C API
#include "botsystem_api.h"
#include <stdio.h>

int main() {
    botsystem_init();
    botsystem_load_plugin("testplugin.so");
    botsystem_send_message("testplugin", "hello");
    botsystem_unload_plugin("testplugin");
    printf("Bot system tests ran (stub)\n");
    return 0;
}
