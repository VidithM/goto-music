#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <omp.h>

#include "types.h"
#include "debug.h"

#define NTHREADS       1
#define MAX_MSG_LEN    256

#define NULL_POINTER  -3
#define PARSE_ERROR   -2
#define OUT_OF_BOUNDS -1
#define SUCCESS        0

#define SILENT         0

int msg_written = 0;
char msg[MAX_MSG_LEN + 1];

#define TRY(func)                           \
{                                           \
    int status = func;                      \
    if(status > 0){                         \
        if(!SILENT){                        \
            printf("[WARNING]: %s\n", msg); \
        }                                   \
    } else if (status < 0){                 \
        if(!SILENT){                        \
            printf("[ERROR]: %s\n", msg);   \
        }                                   \
        exit(0);                            \
    }                                       \
}                                           \

// Util functions
static int64_t write_msg(char *msg_contents){
    size_t msg_len = strlen(msg_contents);
    if(msg_len > MAX_MSG_LEN){
        write_msg("Attempted to write message exceeding max message length\n");
        return OUT_OF_BOUNDS;
    }
    memcpy(msg, msg_contents, sizeof(char) * msg_len);
    return SUCCESS;
}

static int64_t dist(double *res, pair *a, pair *b){
    (*res) = ((a->x - b->x) * (a->x - b->x)) + ((a->y - b->y) * (a->y - b->y));
    return SUCCESS;
}

static int64_t dfs(double *res, tree *t, size_t at, pair *query, int lvl){
    double query_coord = query->x;
    double curr_coord = t->data[at].x;
    if(lvl & 1){
        query_coord = query->y;
        curr_coord = t->data[at].y;
    }
    double curr_dist;
    dist(&curr_dist, query, &t->data[at]);
    (*res) = fmin(*res, curr_dist);

    if(query_coord > curr_coord){
        if(t->has_right[at]){
            TRY(dfs(res, t, t->to_right[at], query, lvl ^ 1));
        }
        if((t->has_left[at]) && ((query_coord - curr_coord) * (query_coord - curr_coord) < (*res))){
            TRY(dfs(res, t, t->to_left[at], query, lvl ^ 1));
        }
    } else {
        if(t->has_left[at]){
            TRY(dfs(res, t, t->to_left[at], query, lvl ^ 1));
        }
        if((t->has_right[at]) && (((query_coord - curr_coord) * (query_coord - curr_coord)) < (*res))){
            TRY(dfs(res, t, t->to_right[at], query, lvl ^ 1));
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
static int64_t tree_init(tree *t, size_t cap){
    if(t == NULL){
        write_msg("Passed null pointer to tree_init");
        return NULL_POINTER;
    }
    t->data = (pair*) malloc(cap * sizeof(pair));
    t->to_left = (size_t*) malloc(cap * sizeof(size_t));
    t->to_right = (size_t*) malloc(cap * sizeof(size_t));
    t->has_left = (int*) malloc(cap * sizeof(int));
    t->has_right = (int*) malloc(cap * sizeof(int));

    memset(t->has_left, 0, cap * sizeof(int));
    memset(t->has_right, 0, cap * sizeof(int));

    t->cap = cap;
    t->nxt_avail = 0;
    return SUCCESS;
}

static int64_t tree_free(tree *t){
    if(t == NULL){
        write_msg("Passed null pointer to tree_free");
        return NULL_POINTER;
    }
    free(t->data);
    free(t->to_left);
    free(t->to_right);
    free(t->has_left);
    free(t->has_right);
    t->cap = t->nxt_avail = 0;
    return SUCCESS;
}

static int64_t tree_add(tree *t, pair *elem){
    if(t == NULL){
        write_msg("Passed null pointer to tree_add");
        return NULL_POINTER;
    }
    if(t->nxt_avail == t->cap){
        write_msg("Called tree_add with a full tree");
        return OUT_OF_BOUNDS;
    }

    int lvl = 0;
    if(t->nxt_avail == 0){
        t->data[0] = *elem;
        t->nxt_avail++;
    } else {
        size_t at = 0;
        while(1){
            double elem_coord = elem->x;
            double curr_coord = t->data[at].x;
            if(lvl & 1){
                elem_coord = elem->y;
                curr_coord = t->data[at].y;
            }
            if(elem_coord < curr_coord){
                if(!t->has_left[at]){
                    t->has_left[at] = 1;
                    t->to_left[at] = t->nxt_avail;
                    t->data[t->nxt_avail] = *elem;
                    t->nxt_avail++;
                    break;
                } else {
                    at = t->to_left[at];
                }
            } else {
                if(!t->has_right[at]){
                    t->has_right[at] = 1;
                    t->to_right[at] = t->nxt_avail;
                    t->data[t->nxt_avail] = *elem;
                    t->nxt_avail++;
                    break;
                } else {
                    at = t->to_right[at];
                }
            }
            lvl ^= 1;
        }
    }
    return SUCCESS;
}

static int64_t tree_query(double *ans, tree *tree, pair *query){
    double res = 1e18;
    TRY(dfs(&res, tree, 0, query, 0));
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
    size_t sample_cap, query_cap;

    if(!PyArg_ParseTuple(args, "ll", &sample_cap, &query_cap)){
        return PyLong_FromLong(PARSE_ERROR);
    }
    TRY(tree_init(&sample, sample_cap));
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
    // printf("adding tree point %0.3f %0.3f\n", x, y);
    TRY(tree_add(&sample, &put));
    return PyLong_FromLong(SUCCESS);
}

static PyObject* add_query(PyObject* self, PyObject* args){
    double x, y;

    if(!PyArg_ParseTuple(args, "dd", &x, &y)){
        return PyLong_FromLong(PARSE_ERROR);
    }
    // printf("adding query point %0.3f %0.3f\n", x, y);
    queries[nqueries].x = x; queries[nqueries].y = y;
    nqueries++;
    // debug_pair_list(queries, nqueries);

    return PyLong_FromLong(SUCCESS);
}
/*
Above functions all return 0 upon success. run_queries is the exception, it returns
the average of all query results
*/
static PyObject* run_queries(PyObject* self, PyObject* args){
    double res = 0;
    // omp_set_num_threads(omp_get_max_threads());
    // #pragma omp parallel for
    for(size_t i = 0; i < nqueries; i++){
        double best;
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