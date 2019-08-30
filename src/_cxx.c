#include <Python.h>
 
static PyObject *get_Neighbourhood()
{
    PyObject *module = PyImport_ImportModule("netomaton");
    if (!module)
      return NULL;
    return PyObject_GetAttrString(module, "Neighbourhood");
}
 
static PyObject* evolve_activities(PyObject* self, PyObject* args)
{
    PyObject *intialConditions; // the list of numbers representing the intial_conditions
    int icLen; // length of the initialConditions
    PyObject *adjacencyMatrix; // the adjacency_matrix argument
    int adjLen; // length of the adjacency_matrix
    int numCells; // the number of items in the first row of the adjacency_matrix
    int timesteps; // the number of timesteps supplied as an argument
    PyObject *activityRule; // the activity_rule lambda
    PyObject *perturbation = NULL; // the perturbation lambda (defaults to None)

    if (!PyArg_ParseTuple(args, "OOiO|O", &intialConditions, &adjacencyMatrix, &timesteps, &activityRule, &perturbation)) {
        return 0;
    }
    
    if (!PyList_Check(intialConditions)) {
        PyErr_SetString(PyExc_TypeError, "a list is required for the initial_conditions");
        return 0;
    }
    
    if (!PyList_Check(adjacencyMatrix)) {
        PyErr_SetString(PyExc_TypeError, "a list is required for the adjacency_matrix");
        return 0;
    }
    
    if (!PyCallable_Check(activityRule)) {
        PyErr_SetString(PyExc_TypeError, "a callable is required for the activity_rule");
        return 0;
    }

    if (perturbation != NULL && !PyCallable_Check(perturbation)) {
        PyErr_SetString(PyExc_TypeError, "a callable is required for the perturbation");
        return 0;
    }

    PyObject *adjSeq = PySequence_Fast(adjacencyMatrix, "expected a sequence");
    adjLen = PySequence_Size(adjacencyMatrix);
    numCells = PySequence_Size(PyList_GetItem(adjSeq, 0));
    printf("adj len: %i\n", adjLen);
    printf("num cells: %i\n", numCells);
    for (unsigned int i = 0; i < adjLen; i++) {
        PyObject *item = PyList_GetItem(adjSeq, i);
        PyObject *adjRowSeq = PySequence_Fast(item, "expected a sequence");
        int cellCount = PySequence_Size(adjRowSeq);
        for (unsigned int j = 0; j < cellCount; j++) {
            PyObject *rowItem = PyList_GetItem(adjRowSeq, j);
            PyObject* repr = PyObject_Repr(rowItem);
            const char* s = PyUnicode_AsUTF8(repr);
            printf("adj val: %i, %s\n", i, s);
            Py_DECREF(repr);
        }
        Py_DECREF(adjRowSeq);
    }
    Py_DECREF(adjSeq);

    printf("timsteps: %i\n", timesteps);

    PyObject *seq = PySequence_Fast(intialConditions, "expected a sequence");
    icLen = PySequence_Size(intialConditions);
    
    // initialize activitiesOverTime
    double** activitiesOverTime;
    activitiesOverTime = malloc(timesteps * sizeof(double*));
    for (int i = 0; i < timesteps; i++) {
        activitiesOverTime[i] = malloc(icLen * sizeof(double));
    }

    for (unsigned int i = 0; i < icLen; i++) {
        PyObject *item = PyList_GetItem(seq, i);
        activitiesOverTime[0][i] = PyFloat_AsDouble(item);
    }
    Py_DECREF(seq);

    for (unsigned int i = 0; i < icLen; i++) {
        printf("aot ic: %i, %f\n", i, activitiesOverTime[0][i]);
    }

    // free activitiesOverTime
    for (int i = 0; i < timesteps; i++) {
        free(activitiesOverTime[i]);
    }
    free(activitiesOverTime);
    
    // build the Neighbourhood activities
    PyObject *activities = PyList_New(3);
    PyList_SetItem(activities, 0, Py_BuildValue("i", 10));
    PyList_SetItem(activities, 1, Py_BuildValue("i", 20));
    PyList_SetItem(activities, 2, Py_BuildValue("i", 30));

    // build the Neighbourhood
    PyObject *neighbourhoodDef = get_Neighbourhood();
    PyObject *neighbourhood = PyObject_CallFunction(neighbourhoodDef, "Oiii", activities, 0, 0, 0);
    if (!neighbourhood)
        return 0;

    // call the activity_rule...
    PyObject *rv = PyObject_CallFunction(activityRule, "O", neighbourhood);

    if (PyLong_Check(rv)) {
        long retVal = PyLong_AsLong(rv);
        printf("ret: %i\n", retVal);
    }

    // if calling it returned 0, must return 0 to propagate the exception
    if (!rv) return 0;
    // otherwise, discard the object returned and return None
    Py_CLEAR(rv);
        
    Py_RETURN_NONE;    
}
 
static PyMethodDef myMethods[] = {
    {"evolve_activities", evolve_activities, METH_VARARGS, "Evolve activities."},
    {NULL, NULL, 0, NULL}
};
 
static struct PyModuleDef _cxx = {
	PyModuleDef_HEAD_INIT,
	"_cxx",
	"Netomaton Extensions Module",
	0,
	myMethods
};

PyMODINIT_FUNC PyInit__cxx(void)
{
    return PyModule_Create(&_cxx);
}