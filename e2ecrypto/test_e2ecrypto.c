// test_e2ecrypto.c
// Test stub for VRBLL E2E crypto C API
#include "e2ecrypto_api.h"
#include <stdio.h>

int main() {
    e2ecrypto_init();
    char pubkey[256], privkey[256];
    e2ecrypto_generate_keys(pubkey, sizeof(pubkey), privkey, sizeof(privkey));
    char ciphertext[512], plaintext[512] = "secret message";
    e2ecrypto_encrypt(plaintext, pubkey, ciphertext, sizeof(ciphertext));
    char decrypted[512];
    e2ecrypto_decrypt(ciphertext, privkey, decrypted, sizeof(decrypted));
    printf("E2E crypto tests ran (stub)\n");
    return 0;
}
