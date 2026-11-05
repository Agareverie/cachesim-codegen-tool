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
#define INDEXLEN 8
#define OFFSETLEN 2
#define INDEX_SIZE (1 << (INDEXLEN))         // 2^INDEXLEN
#define BLOCK_SIZE (1 << (OFFSETLEN))        // 2^OFFSETLEN
#define CACHE_SIZE (INDEX_SIZE * BLOCK_SIZE) // INDEXLEN = log2(CACHE_SIZE) - log2(BLOCK_SIZE)
#define TAGLEN (32 - (INDEXLEN + OFFSETLEN))

typedef unsigned char Byte;
typedef struct Cache {
    bool valid;
    bool dirty;
    unsigned long tag;
    Byte data[BLOCK_SIZE];
} Cache;

#endif // CACHESIM_H_INCLUDED
