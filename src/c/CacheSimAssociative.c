/**
 * CacheSim.c
 * This program is designed for class exercise only.
 * It is provided as is. There is no warranty or support of any kind.
 *
 * Krerk Piromsopa, Ph.D.
 * Department of Computer Engineering
 * Chulalongkorn University
 * Bangkok, Thailand.
 *
 * History
 * 2013 - Initial design
 * 2015 - Refactor/Clean code
 **/
#include "CacheSimAssociative.h"
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

long MISS;
long HIT;
struct Cache caches[INDEX_SIZE][ASSOCIATIVITY];

// tracks the current index to be replaced for each cache in round robin mode
int roundRobin[INDEX_SIZE];

// tracks the last used time of each cache
int lastUsedTime[INDEX_SIZE][ASSOCIATIVITY];

// the "time" incremented once per update
int time = 0;
int getMinIndex(int length, int *arr) {
    int min = arr[0];
    int index = 0;
    for (int i = 1; i < length; i++) {
        int value = arr[i];
        if (value < min) {
            min = value;
            index = i;
        }
    }

    return index;
}

void init(void) {
    for (int i = 0; i < INDEX_SIZE; i++) {
        for (int j = 0; j < ASSOCIATIVITY; j++) {
            caches[i][j].valid = 0;
            caches[i][j].tag = 0;
            caches[i][j].dirty = 0;

            lastUsedTime[i][j] = 0;
        }

        roundRobin[i] = 0;
    }
    MISS = 0;
    HIT = 0;
}

void calAddr(unsigned long addr, unsigned long *tag, unsigned long *idx, unsigned long *offset) {
    unsigned long tmp;
    int i;
    *tag = addr >> (OFFSETLEN + INDEXLEN);
    tmp = 0;
    for (i = 0; i < INDEXLEN; i++) {
        tmp <<= 1;
        tmp |= 0x01;
    }
    *idx = addr >> OFFSETLEN & tmp;
    tmp = 0;
    for (i = 0; i < OFFSETLEN; i++) {
        tmp <<= 1;
        tmp |= 0x01;
    }
    *offset = addr & tmp;
}

void access(unsigned long addr) {
    unsigned long offset;
    unsigned long tag;
    unsigned long idx;
    calAddr(addr, &tag, &idx, &offset);
    bool hit = false;
    for (int i = 0; i < ASSOCIATIVITY; i++) {
        struct Cache cache = caches[idx][i];
        if (cache.tag == tag && cache.valid) {
            HIT++;
            hit = true;

            lastUsedTime[idx][i] = time;
            break;
        }
    }
    if (!hit) {
        MISS++;
        struct Cache cache;
        cache.valid = 1;
        cache.tag = tag;

        // round robin
        if (USE_ROUND_ROBIN) {
            caches[idx][roundRobin[idx]] = cache;
            roundRobin[idx] = (roundRobin[idx] + 1) % ASSOCIATIVITY;
        }
        // least recently used
        else {
            int leastRecentlyUsedIndex = getMinIndex(ASSOCIATIVITY, lastUsedTime[idx]);
            caches[idx][leastRecentlyUsedIndex] = cache;
            lastUsedTime[idx][leastRecentlyUsedIndex] = time;
        }
    }
    // else{
    // MISS++;
    // cache[idx].valid=1;
    // cache[idx].tag = tag;
    // }
    time++;
}

double hit_rate(long hit, long miss) {
    return (double)hit / (hit + miss);
}

int main(int argc, char *argv[]) {
    printf("CacheSim v.2015\n");
    printf("This program is designed for class exercise only.\n");
    printf("By Krerk Piromsopa, Ph.D.\n");
    init();
    FILE *input;
    char buff[1025];
    unsigned long myaddr;
    if (argc < 2) {
        fprintf(stderr, "Usage:\n\t%s address_file\n", argv[0]);
        exit(-1);
    }
    input = fopen(argv[1], "r");
    // read file
    while (fgets(&buff[0], 1024, input)) {
        sscanf(buff, "0x%lx", &myaddr);
        access(myaddr);
    }
    printf("Replacement Algorithm: ");
    if (USE_ROUND_ROBIN) {
        printf("round-robin\n");
    } else {
        printf("least-recently-used\n");
    }

    printf("Cache Size = %d Bytes = %d Kibibytes\n", CACHE_SIZE, (CACHE_SIZE / 1024));
    printf("Block Size = %d\n", BLOCK_SIZE);
    printf("Associativity = %d\n", ASSOCIATIVITY);
    printf("Hit = %ld, Miss = %ld\n", HIT, MISS);
    printf("Hit Rate = %.7f\n", hit_rate(HIT, MISS));
}
