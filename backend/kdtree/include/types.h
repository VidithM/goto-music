#pragma once

#include <stddef.h>

// Structs
typedef struct pair {
    double x;
    double y;
} pair;

typedef struct tree {
    pair *data;
    size_t *to_left, *to_right;
    size_t nxt_avail;
    size_t cap;
} tree;