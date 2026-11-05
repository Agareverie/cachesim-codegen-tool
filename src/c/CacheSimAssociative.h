/**
 * CacheSim.h
 * This program is designed for class exercise only.
 * It is provided as is. There is no warranty or support of any kind.
 *
 * Krerk Piromsopa, Ph.D.
 * Department of Computer Engineering
 * Chulalongkorn University
 * Bangkok, Thailand.
 **/
#ifndef CACHESIM_H_INCLUDED
#define CACHESIM_H_INCLUDED
#include <stdbool.h>

/* Please adjust parameters here */
#define CACHE_SIZE ((INDEX_SIZE * BLOCK_SIZE) * ASSOCIATIVITY) // 1024
#define INDEX_SIZE 1 << (INDEXLEN)                             // 256
#define BLOCK_SIZE 1 << (OFFSETLEN)                            // 4
#define TAGLEN 32 - (INDEXLEN + OFFSETLEN)                     // 22
#define INDEXLEN 18 - OFFSETLEN                                // 8
#define OFFSETLEN 2                                            // 2

#define ASSOCIATIVITY 4
#define USE_ROUND_ROBIN true

typedef unsigned char Byte;
typedef struct Cache {
    bool valid;
    bool dirty;
    unsigned long tag;
    Byte data[BLOCK_SIZE];
} Cache;

#endif // CACHESIM_H_INCLUDED
