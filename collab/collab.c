// collab.c
// Minimal collaboration tools implementation for VRBLL (C)
#include "collab_api.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define DOC_FILE_PREFIX "vrbll_doc_"

int collab_init(void) {
    // No-op for demo
    return 0;
}

int collab_create_doc(const char* doc_id) {
    char filename[256];
    snprintf(filename, sizeof(filename), "%s%s.txt", DOC_FILE_PREFIX, doc_id);
    FILE* f = fopen(filename, "w");
    if (!f) return -1;
    fclose(f);
    return 0;
}

int collab_edit_doc(const char* doc_id, const char* user, const char* content) {
    char filename[256];
    snprintf(filename, sizeof(filename), "%s%s.txt", DOC_FILE_PREFIX, doc_id);
    FILE* f = fopen(filename, "a");
    if (!f) return -1;
    fprintf(f, "%s: %s\n", user, content);
    fclose(f);
    return 0;
}

int collab_get_doc(const char* doc_id, char* buffer, size_t bufsize) {
    char filename[256];
    snprintf(filename, sizeof(filename), "%s%s.txt", DOC_FILE_PREFIX, doc_id);
    FILE* f = fopen(filename, "r");
    if (!f) return -1;
    size_t used = 0;
    char line[256];
    while (fgets(line, sizeof(line), f)) {
        int n = snprintf(buffer + used, bufsize - used, "%s", line);
        if (n < 0 || (used + n) >= bufsize) break;
        used += n;
    }
    fclose(f);
    return (int)used;
}
