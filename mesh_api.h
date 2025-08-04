// VRBLL Mesh & API Integration (C)
#ifndef VRBLL_MESH_API_H
#define VRBLL_MESH_API_H
void mesh_send(const void* data, int len);
void mesh_recv(void* buf, int maxlen);
#endif
