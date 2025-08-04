// e2ecrypto_api.h
// End-to-end encryption API for VRBLL (C)
#ifndef E2ECRYPTO_API_H
#define E2ECRYPTO_API_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

// Initialize E2E crypto
int e2ecrypto_init(void);

// Generate key pair
int e2ecrypto_generate_keys(char* pubkey, size_t pubkey_size, char* privkey, size_t privkey_size);

// Encrypt message
int e2ecrypto_encrypt(const char* plaintext, const char* pubkey, char* ciphertext, size_t bufsize);

// Decrypt message
int e2ecrypto_decrypt(const char* ciphertext, const char* privkey, char* plaintext, size_t bufsize);

#ifdef __cplusplus
}
#endif

#endif // E2ECRYPTO_API_H
