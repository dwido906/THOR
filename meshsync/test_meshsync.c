// test_meshsync.c
// Test stub for VRBLL mesh sync C API
#include "meshsync_api.h"
#include <stdio.h>

int main() {
    if (meshsync_init("testnode") != 0) {
        printf("Mesh sync init failed\n");
        return 1;
    }
    meshsync_discover_peers();
    char data[] = "testdata";
    meshsync_sync_data(data, sizeof(data));
    meshsync_handle_incoming(data, sizeof(data));
    printf("Mesh sync tests ran (stub)\n");
    return 0;
}
