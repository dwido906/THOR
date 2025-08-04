// aimoderation_api.h
// AI-powered moderation API for VRBLL (C)
#ifndef AIMODERATION_API_H
#define AIMODERATION_API_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

// Initialize AI moderation
int aimoderation_init(void);

// Moderate a message (returns 0=ok, 1=flagged)
int aimoderation_moderate_message(const char* user, const char* message, char* reason, size_t reason_size);

// Moderate a voice packet (returns 0=ok, 1=flagged)
int aimoderation_moderate_voice(const void* data, size_t size, char* reason, size_t reason_size);

#ifdef __cplusplus
}
#endif

#endif // AIMODERATION_API_H
