#include "debug.h"

void debug_pair_list(pair *pairs, size_t npairs){
    printf("*** [DEBUG] printing pair list of length %zu ***\n", npairs);
    for(size_t i = 0; i < npairs; i++){
        printf("*** [DEBUG] index (%zu) has value (%0.3f, %0.3f) ***\n", i, pairs[i].x, pairs[i].y);
    }
}

void debug_tree(tree *tree){
    printf("*** [DEBUG] printing tree with %zu cap and %zu points\n", tree->cap, tree->npts);
    
}