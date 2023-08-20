#pragma once

#include <stddef.h>

// Structs
typedef struct pair {
    double x;
    double y;
} pair;

typedef struct tree {
    struct tree *left, *right;
    int init;
    pair data;
} tree;