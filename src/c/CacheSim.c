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
#include "CacheSim.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

long MISS;
long HIT;
struct Cache cache[INDEX_SIZE];
void init(void) {
    MISS = 0;
    HIT = 0;
    int i;
    for (i = 0; i < INDEX_SIZE; i++) {
        cache[i].valid = 0;
        cache[i].tag = 0;
        cache[i].dirty = 0;
    }
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
    // For cache in caches
    if (cache[idx].tag == tag && cache[idx].valid) {
        HIT++;
    } else {
        // implement the replacement algorithm
        MISS++;
        cache[idx].valid = 1;
        cache[idx].tag = tag;
    }
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
    printf("Replacement Algorithm: direct-mapped\n");
    printf("Cache Size = %d Bytes = %d Kibibytes\n", CACHE_SIZE, (CACHE_SIZE / 1024));
    printf("Block Size = %d\n", BLOCK_SIZE);
    printf("Associativity = 1\n");
    printf("Hit = %ld, Miss = %ld\n", HIT, MISS);
    printf("Hit Rate = %.7f\n", hit_rate(HIT, MISS));
}
