// aimoderation.c
// Minimal AI-powered moderation implementation for VRBLL (C)
#include "aimoderation_api.h"
#include <stdio.h>
#include <string.h>

// Simple keyword list for demo
static const char* banned_words[] = {"spam", "abuse", "toxic", NULL};

int aimoderation_init(void) {
    // No-op for demo
    return 0;
}

int aimoderation_moderate_message(const char* user, const char* message, char* reason, size_t reason_size) {
    for (int i = 0; banned_words[i]; ++i) {
        if (strstr(message, banned_words[i])) {
            snprintf(reason, reason_size, "Flagged for '%s'", banned_words[i]);
            return 1;
        }
    }
    snprintf(reason, reason_size, "OK");
    return 0;
}

int aimoderation_moderate_voice(const void* data, size_t size, char* reason, size_t reason_size) {
    // For demo, always OK
    snprintf(reason, reason_size, "OK");
    return 0;
}
