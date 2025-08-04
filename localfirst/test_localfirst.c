// test_localfirst.c
// Test stub for VRBLL local-first C API
#include "localfirst_api.h"
#include <stdio.h>

int main() {
    if (localfirst_init("testdb.vrbll") != 0) {
        printf("Init failed\n");
        return 1;
    }
    localfirst_store_message("general", "alice", "Hello, world!", 1234567890);
    char buf[1024];
    localfirst_get_messages("general", buf, sizeof(buf));
    localfirst_sync();
    localfirst_resolve_conflicts();
    printf("Local-first tests ran (stub)\n");
    return 0;
}
