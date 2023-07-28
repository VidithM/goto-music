#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <omp.h>

#define DEFAULT_CAP 10

typedef struct pair {
    double x;
    double y;
} pair;

typedef struct plist {
    size_t len, cap;
    pair* data;
} plist;

static int init = 0;
static struct plist queries, points;

void plist_init(plist* list){
    list->data = (pair*) malloc(DEFAULT_CAP * sizeof(pair));
    list->cap = DEFAULT_CAP;
}

void plist_add(plist* list){
    
}

static PyObject* add_point(PyObject *self, PyObject *args){
    return PyLong_FromLong(0);
}

static PyObject* add_query(PyObject *self, PyObject *args){
    return PyLong_FromLong(0);
}

static PyObject* run_queries(PyObject *self, PyObject *args){
    return PyLong_FromLong(0);
}

static PyMethodDef export_methods[] = {
    {"add_point", add_point, METH_VARARGS, "Add a reference point"},
    {"add_query", add_query, METH_VARARGS, "Add a query point"},
    {"run_queries", run_queries, METH_VARARGS, "Run added queries"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "kdtree",
    "Parallel KD Tree",
    -1,
    export_methods
};

PyMODINIT_FUNC PyInit_module(){
    return PyModule_Create(&module);
}