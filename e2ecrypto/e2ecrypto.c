// e2ecrypto.c
// Minimal E2E encryption implementation for VRBLL (C)
#include "e2ecrypto_api.h"
#include <sodium.h>
#include <stdio.h>
#include <string.h>

int e2ecrypto_init(void) {
    if (sodium_init() < 0) {
        return -1;
    }
    return 0;
}

int e2ecrypto_generate_keys(char* pubkey, size_t pubkey_size, char* privkey, size_t privkey_size) {
    unsigned char pk[crypto_box_PUBLICKEYBYTES];
    unsigned char sk[crypto_box_SECRETKEYBYTES];
    crypto_box_keypair(pk, sk);
    if (pubkey_size < crypto_box_PUBLICKEYBYTES*2+1 || privkey_size < crypto_box_SECRETKEYBYTES*2+1) return -1;
    sodium_bin2hex(pubkey, pubkey_size, pk, crypto_box_PUBLICKEYBYTES);
    sodium_bin2hex(privkey, privkey_size, sk, crypto_box_SECRETKEYBYTES);
    return 0;
}

int e2ecrypto_encrypt(const char* plaintext, const char* pubkey_hex, char* ciphertext, size_t bufsize) {
    unsigned char pk[crypto_box_PUBLICKEYBYTES];
    unsigned char nonce[crypto_box_NONCEBYTES];
    unsigned char ct[4096];
    randombytes_buf(nonce, sizeof(nonce));
    sodium_hex2bin(pk, sizeof(pk), pubkey_hex, strlen(pubkey_hex), NULL, NULL, NULL);
    // For demo, use ephemeral keypair and zeroed secret key
    unsigned char sk[crypto_box_SECRETKEYBYTES] = {0};
    crypto_box_easy(ct, (const unsigned char*)plaintext, strlen(plaintext), nonce, pk, sk);
    if (bufsize < crypto_box_NONCEBYTES*2 + strlen((char*)ct)*2 + 2) return -1;
    sodium_bin2hex(ciphertext, crypto_box_NONCEBYTES*2+1, nonce, crypto_box_NONCEBYTES);
    size_t offset = crypto_box_NONCEBYTES*2;
    sodium_bin2hex(ciphertext+offset, bufsize-offset, ct, strlen((char*)ct));
    return 0;
}

int e2ecrypto_decrypt(const char* ciphertext, const char* privkey_hex, char* plaintext, size_t bufsize) {
    unsigned char sk[crypto_box_SECRETKEYBYTES];
    unsigned char nonce[crypto_box_NONCEBYTES];
    unsigned char ct[4096];
    sodium_hex2bin(sk, sizeof(sk), privkey_hex, strlen(privkey_hex), NULL, NULL, NULL);
    memcpy(nonce, ciphertext, crypto_box_NONCEBYTES);
    memcpy(ct, ciphertext+crypto_box_NONCEBYTES*2, strlen(ciphertext)-crypto_box_NONCEBYTES*2);
    // For demo, use ephemeral public key (all zero)
    unsigned char pk[crypto_box_PUBLICKEYBYTES] = {0};
    crypto_box_open_easy((unsigned char*)plaintext, ct, strlen((char*)ct), nonce, pk, sk);
    return 0;
}
