// localfirst.c
// Minimal local-first storage implementation for VRBLL (C)
#include "localfirst_api.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define DB_FILE "vrbll_local.db"

static FILE* db = NULL;

int localfirst_init(const char* db_path) {
    db = fopen(db_path ? db_path : DB_FILE, "a+");
    return db ? 0 : -1;
}

int localfirst_store_message(const char* channel, const char* user, const char* message, uint64_t timestamp) {
    if (!db) return -1;
    fseek(db, 0, SEEK_END);
    fprintf(db, "%s|%s|%s|%llu\n", channel, user, message, (unsigned long long)timestamp);
    fflush(db);
    return 0;
}

int localfirst_get_messages(const char* channel, char* buffer, size_t bufsize) {
    if (!db) return -1;
    rewind(db);
    size_t used = 0;
    char line[512];
    while (fgets(line, sizeof(line), db)) {
        char ch[64], user[64], msg[256];
        unsigned long long ts;
        if (sscanf(line, "%63[^|]|%63[^|]|%255[^|]|%llu", ch, user, msg, &ts) == 4) {
            if (strcmp(ch, channel) == 0) {
                int n = snprintf(buffer + used, bufsize - used, "%s|%s|%s|%llu\n", ch, user, msg, ts);
                if (n < 0 || (used + n) >= bufsize) break;
                used += n;
            }
        }
    }
    return (int)used;
}

int localfirst_sync(void) {
    // Stub: mesh/remote sync not implemented
    return 0;
}

int localfirst_resolve_conflicts(void) {
    // Stub: conflict resolution not implemented
    return 0;
}
