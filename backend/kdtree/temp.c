#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <omp.h>

#define OUT_OF_BOUNDS -1
#define SUCCESS        0

typedef struct pair {
    double x;
    double y;
} pair;

typedef struct tree {
    size_t cap;
    pair *data;
    int *init;
} tree;

static int do_free = 0;

static tree sample;
static pair* queries;

static uint64_t tree_init(tree *tree, size_t cap){
    tree->data = (pair*) malloc(cap * sizeof(pair));
    tree->init = (int*) malloc(cap * sizeof(int));
    memset(tree->init, 0, cap * sizeof(int));
    tree->cap = cap;
    return SUCCESS;
}

static uint64_t tree_free(tree *tree){
    free(tree->data);
    free(tree->init);
    tree->cap = 0;
    return SUCCESS;
}

static uint64_t tree_add(tree *tree, pair *elem){
    int lvl = 0;
    size_t at = 1;
    while(1){
        double elem_coord = elem->x;
        double curr_coord = tree->data[at].x;
        if(lvl & 1){
            elem_coord = elem->y;
            curr_coord = tree->data[at].y;
        }
        if(elem_coord < curr_coord){
            if(!tree->init[at << 1]){
                tree->data[at << 1] = *elem;
                tree->init[at << 1] = 1;
                break;
            } else {
                at <<= 1;
            }
        } else {
            if(!tree->init[(at << 1) + 1]){
                tree->data[(at << 1) + 1] = *elem;
                tree->init[(at << 1) + 1] = 1;
                break;
            } else {
                at <<= 1; at++;
            }
        }
    }
}

static uint64_t tree_query(pair *res, tree *tree, pair *query){

}

static uint64_t dist(double *res, pair *a, pair *b){
    (*res) = (a->x * a->x) + (a->y * a->y);
}

static PyObject* reset(PyObject* self, PyObject* args){
    if(do_free){
        tree_free(&sample);
        free(queries);
    }
    do_free = 1;
    // TODO: read this from args
    size_t cap = 1;
    tree_init(&sample, cap);
    return PyLong_FromLong(SUCCESS);
}

static PyObject* add_point(PyObject* self, PyObject* args){
    return PyLong_FromLong(SUCCESS);
}

static PyObject* add_query(PyObject* self, PyObject* args){
    return PyLong_FromLong(SUCCESS);
}

static PyObject* run_queries(PyObject* self, PyObject* args){
    return PyLong_FromLong(SUCCESS);
}

static PyMethodDef export_methods[] = {
    {"add_point", add_point, METH_VARARGS, "Add a reference point"},
    {"add_query", add_query, METH_VARARGS, "Add a query point"},
    {"run_queries", run_queries, METH_VARARGS, "Run added queries"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "tree",
    "Parallel KD Tree",
    -1,
    export_methods
};

PyMODINIT_FUNC PyInit_module(){
    return PyModule_Create(&module);
}