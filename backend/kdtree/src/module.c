#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <omp.h>

#include "types.h"
#include "debug.h"

#define NTHREADS       1
#define MAX_MSG_LEN    256

#define PARSE_ERROR   -2
#define OUT_OF_BOUNDS -1
#define SUCCESS        0

int msg_written = 0;
char msg[MAX_MSG_LEN];

#define TRY(status)                         \
{                                           \
    if(status > 0){                         \
        printf("[WARNING]: %s\n", msg);     \
    } else if (status < 0){                 \
        printf("[ERROR]: %s\n", msg);       \
        exit(0);                            \
    }                                       \
}                                           \

// Util functions
static uint64_t dist(double *res, pair *a, pair *b){
    (*res) = (a->x * a->x) + (a->y * a->y);
    return SUCCESS;
}

static uint64_t dfs(double *res, tree *tree, pair *query, size_t at, int lvl){
    printf("in dfs %d %d\n", lvl, tree->init[at]);
    double query_coord = query->x;
    double curr_coord = tree->data[at].x;
    if(lvl & 1){
        query_coord = query->y;
        curr_coord = tree->data[at].y;
    }
    double curr_dist;
    dist(&curr_dist, query, tree->data + at);
    (*res) = fmin(*res, curr_dist);

    // TODO: add bounds checking

    if(query_coord > curr_coord){
        if(tree->init[at << 1]){
            TRY(dfs(res, tree, query, at << 1, lvl ^ 1));
        }
        if((tree->init[(at << 1) + 1]) && ((query_coord - curr_coord) * (query_coord - curr_coord)) < (*res)){
            TRY(dfs(res, tree, query, (at << 1) + 1, lvl ^ 1));
        }
    } else {
        if(tree->init[(at << 1) + 1]){
            TRY(dfs(res, tree, query, (at << 1) + 1, lvl ^ 1));
        }
        if((tree->init[at << 1]) && ((query_coord - curr_coord) * (query_coord - curr_coord)) < (*res)){
            TRY(dfs(res, tree, query, at << 1, lvl ^ 1));
        }
    }
    return SUCCESS;
}

// Global state
static int do_free = 0;

static tree sample;

static pair *queries;
static size_t nqueries = 0;

// Internal functions
static uint64_t tree_init(tree *tree, size_t cap){
    tree->data = (pair*) malloc(cap * sizeof(pair));
    tree->init = (int*) malloc(cap * sizeof(int));
    memset(tree->init, 0, cap * sizeof(int));
    tree->cap = cap;
    tree->npts = 0;
    return SUCCESS;
}

static uint64_t tree_free(tree *tree){
    free(tree->data);
    free(tree->init);
    tree->cap = 0;
    tree->npts = 0;
    return SUCCESS;
}

static uint64_t tree_add(tree *tree, pair *elem){
    int lvl = 0;
    size_t at = 1;
    printf("here %d\n", tree->init[1]);
    if(!tree->init[1]){
        tree->init[1] = 1;
        tree->data[1] = *elem;
    } else {
        while(1){
            printf("passed here when adding\n");
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
            lvl ^= 1;
        }
    }
    return SUCCESS;
}

static uint64_t tree_query(double *ans, tree *tree, pair *query){
    double res = 1e18;
    TRY(dfs(&res, tree, query, 1, 0));
    // printf("%0.3f\n", res);
    (*ans) = res;
    return SUCCESS;
}

// Module functions (exposed to Python)
static PyObject* reset(PyObject* self, PyObject* args){
    if(do_free){
        TRY(tree_free(&sample));
        free(queries);
    }
    do_free = 1;
    size_t tree_cap, query_cap;

    if(!PyArg_ParseTuple(args, "ll", &tree_cap, &query_cap)){
        return PyLong_FromLong(PARSE_ERROR);
    }

    TRY(tree_init(&sample, tree_cap));
    queries = (pair*) malloc(query_cap * sizeof(pair));
    nqueries = 0;

    return PyLong_FromLong(SUCCESS);
}

static PyObject* add_point(PyObject* self, PyObject* args){
    double x, y;
    if(!PyArg_ParseTuple(args, "dd", &x, &y)){
        return PyLong_FromLong(PARSE_ERROR);
    }
    pair put; put.x = x; put.y = y;
    printf("adding tree point %0.3f %0.3f\n", x, y);
    TRY(tree_add(&sample, &put));
    sample.npts++;
    return PyLong_FromLong(SUCCESS);
}

static PyObject* add_query(PyObject* self, PyObject* args){
    double x, y;

    if(!PyArg_ParseTuple(args, "dd", &x, &y)){
        return PyLong_FromLong(PARSE_ERROR);
    }
    printf("adding query point %0.3f %0.3f\n", x, y);
    queries[nqueries].x = x; queries[nqueries].y = y;
    nqueries++;
    debug_pair_list(queries, nqueries);

    return PyLong_FromLong(SUCCESS);
}
/*
Above functions all return 0 upon success. run_queries is the exception, it returns
the average of all query results
*/
static PyObject* run_queries(PyObject* self, PyObject* args){
    double res = 0;
    for(size_t i = 0; i < nqueries; i++){
        double best;
        printf("calling query\n");
        TRY(tree_query(&best, &sample, &queries[i]));
        res += best;
    }
    res /= nqueries;
    return Py_BuildValue("d", res);
}

// Module definitions
static PyObject* version(PyObject* self){
    return Py_BuildValue("s", "1.0");
}

static PyMethodDef export_methods[] = {
    {"reset", reset, METH_VARARGS, "Reset the tree"},
    {"add_point", add_point, METH_VARARGS, "Add a reference point"},
    {"add_query", add_query, METH_VARARGS, "Add a query point"},
    {"run_queries", run_queries, METH_VARARGS, "Run added queries"},
    {"version", (PyCFunction) version, METH_NOARGS, "Current extension version"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "pkd",
    "Parallel KD Tree",
    -1,
    export_methods
};

PyMODINIT_FUNC PyInit_pkd(){
    return PyModule_Create(&module);
}