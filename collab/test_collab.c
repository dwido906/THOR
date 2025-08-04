// test_collab.c
// Test stub for VRBLL collaboration C API
#include "collab_api.h"
#include <stdio.h>

int main() {
    collab_init();
    collab_create_doc("doc1");
    collab_edit_doc("doc1", "alice", "Hello, world!");
    char buf[1024];
    collab_get_doc("doc1", buf, sizeof(buf));
    printf("Collab tests ran (stub)\n");
    return 0;
}
