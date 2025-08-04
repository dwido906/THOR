// collab_api.h
// Collaboration tools API for VRBLL (C)
#ifndef COLLAB_API_H
#define COLLAB_API_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

// Initialize collaboration tools
int collab_init(void);

// Create a shared document
int collab_create_doc(const char* doc_id);

// Edit a document
int collab_edit_doc(const char* doc_id, const char* user, const char* content);

// Get document content
int collab_get_doc(const char* doc_id, char* buffer, size_t bufsize);

#ifdef __cplusplus
}
#endif

#endif // COLLAB_API_H
