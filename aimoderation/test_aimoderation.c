// test_aimoderation.c
// Test stub for VRBLL AI moderation C API
#include "aimoderation_api.h"
#include <stdio.h>

int main() {
    aimoderation_init();
    char reason[256];
    int flagged = aimoderation_moderate_message("alice", "test message", reason, sizeof(reason));
    aimoderation_moderate_voice("voice", 5, reason, sizeof(reason));
    printf("AI moderation tests ran (stub), flagged=%d\n", flagged);
    return 0;
}
