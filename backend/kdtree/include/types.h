#pragma once

#include <stddef.h>

// Structs
typedef struct pair {
    double x;
    double y;
} pair;

typedef struct tree {
    size_t cap, npts;
    pair *data;
    int *init;
} tree;