#include <Python.h>

typedef struct {
    int size;
    int capacity;
    int* items;
} IntList;

static IntList newList() {
    IntList list;
    list.size = 0;
    list.capacity = 10;

    list.items = malloc(list.capacity * sizeof(int));
    memset(list.items, 0, list.capacity * sizeof(int));

    return list;
}

static void addInt(int v, IntList *list) {
    if ((list->size + 1) == list->capacity) {
        realloc(list->items, list->size * 2);
        list->capacity = list->size * 2;
    }
    list->items[list->size] = v;
    list->size++;
}

static void freeList(IntList *list) {
    free(list->items);
}

static PyObject *getNeighbourhood()
{
    PyObject *module = PyImport_ImportModule("netomaton");
    if (!module)
      return NULL;
    PyObject *n = PyObject_GetAttrString(module, "Neighbourhood");
    Py_DECREF(module);
    return n;
}

static PyObject *getActivities(IntList *indices, double *lastActivities) {
    PyObject *activities = PyList_New(indices->size);
    for (unsigned int i = 0; i < indices->size; i++) {
        PyList_SetItem(activities, i, Py_BuildValue("d", lastActivities[indices->items[i]]));
    }
    return activities;
}

static PyObject *getCellIndices(IntList *indices) {
    PyObject *cellIndices = PyList_New(indices->size);
    for (unsigned int i = 0; i < indices->size; i++) {
        PyList_SetItem(cellIndices, i, Py_BuildValue("i", indices->items[i]));
    }
    return cellIndices;
}

static PyObject *getWeights(IntList *indices, PyObject *adjSeq, int cellIndex) {
    // adjSeq is the sequence with the adjancency matrix rows
    PyObject *weights = PyList_New(indices->size);
    for (unsigned int i = 0; i < indices->size; i++) {
        int fromIndex = indices->items[i];
        PyObject *item = PyList_GetItem(adjSeq, fromIndex);
        PyObject *adjRowSeq = PySequence_Fast(item, "expected a sequence");
        PyObject *rowItem = PyList_GetItem(adjRowSeq, cellIndex);
        double weight = PyFloat_AsDouble(rowItem);
        PyList_SetItem(weights, i, Py_BuildValue("d", weight));
    }
    return weights;
}

static PyObject *buildActivities(double** activitiesOverTime, int timesteps, int numCells) {
    PyObject *activities = PyList_New(timesteps);
    for (unsigned int t = 0; t < timesteps; t++) {
        PyObject *activitiesAtT = PyList_New(numCells);
        for (unsigned int c = 0; c < numCells; c++) {
            PyList_SetItem(activitiesAtT, c, Py_BuildValue("d", activitiesOverTime[t][c]));
        }
        PyList_SetItem(activities, t, activitiesAtT);
    }
    return activities;
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

    PyObject *seq = PySequence_Fast(intialConditions, "expected a sequence");
    icLen = PySequence_Size(intialConditions);
    
    // initialize activitiesOverTime
    double** activitiesOverTime = malloc(timesteps * sizeof(double*));
    memset(activitiesOverTime, 0.0, timesteps * sizeof(double*));
    for (int i = 0; i < timesteps; i++) {
        activitiesOverTime[i] = malloc(icLen * sizeof(double));
        memset(activitiesOverTime[i], 0.0, icLen * sizeof(double));
    }

    for (unsigned int i = 0; i < icLen; i++) {
        PyObject *item = PyList_GetItem(seq, i);
        if (PyNumber_Check(item)) {
            PyObject* pyFloat = PyNumber_Float(item);    
            if (!pyFloat) {
                PyErr_SetString(PyExc_RuntimeError, "could not convert initial condition value to a double");
                return 0;
            }
            activitiesOverTime[0][i] = PyFloat_AsDouble(pyFloat);
        } else {
            PyErr_SetString(PyExc_RuntimeError, "initial conditions must contain only numbers");
            return 0;
        }
    }
    Py_DECREF(seq);

    PyObject *adjSeq = PySequence_Fast(adjacencyMatrix, "expected a sequence");
    adjLen = PySequence_Size(adjacencyMatrix);
    numCells = PySequence_Size(PyList_GetItem(adjSeq, 0));
    // build a map of cell index -> list of cell indices that point to it
    //  - the array index will act as the key (i.e. the map will be just an array; 
    //    e.g. the entry at the 0th position is the value for the first cell)
    //  - each entry in the array is an IntList, of potentially any length
    //  - each int in the IntList is the index of a cell that points to the cell given by the array index of the IntList
    IntList* nonZeroIndexMap = malloc(numCells * sizeof(IntList));
    for (unsigned int c = 0; c < numCells; c++) {
        nonZeroIndexMap[c] = newList();
        for (unsigned int row = 0; row < adjLen; row++) {
            PyObject *item = PyList_GetItem(adjSeq, row);
            PyObject *adjRowSeq = PySequence_Fast(item, "expected a sequence");
            PyObject *rowItem = PyList_GetItem(adjRowSeq, c);

            double weight = 0.0;
            if (PyNumber_Check(rowItem)) {
                PyObject* pyFloat = PyNumber_Float(rowItem);    
                if (!pyFloat) {
                    PyErr_SetString(PyExc_RuntimeError, "could not convert weight value to a double");
                    return 0;
                }
                weight = PyFloat_AsDouble(pyFloat);
            } else {
                PyErr_SetString(PyExc_RuntimeError, "weights must consist only of numbers");
                return 0;
            }

            if (weight != 0.0) {
                addInt(row, &nonZeroIndexMap[c]);
            }
            
            Py_DECREF(adjRowSeq);
        }
    }

    // perform the the evolution...
    for (unsigned int t = 1; t < timesteps; t++) {
        double* lastActivities = activitiesOverTime[t - 1];

        for (unsigned int c = 0; c < numCells; c++) {
            PyObject *activities = getActivities(&nonZeroIndexMap[c], lastActivities);
            PyObject *cellIndices = getCellIndices(&nonZeroIndexMap[c]);
            PyObject *weights = getWeights(&nonZeroIndexMap[c], adjSeq, c);
            double lastActivity = lastActivities[c];

            // build the Neighbourhood
            PyObject *neighbourhoodDef = getNeighbourhood();
            PyObject *neighbourhood = PyObject_CallFunction(neighbourhoodDef, "OOOd", activities, cellIndices, weights, lastActivity);
            if (!neighbourhood) {
                PyErr_SetString(PyExc_RuntimeError, "could not create Neighbourhood");
                return 0;
            }

            // call the activity_rule...
            PyObject *activityRuleArgs = PyTuple_New(3);
            PyTuple_SetItem(activityRuleArgs, 0, Py_BuildValue("O", neighbourhood));
            PyTuple_SetItem(activityRuleArgs, 1, Py_BuildValue("i", c));
            PyTuple_SetItem(activityRuleArgs, 2, Py_BuildValue("i", t));
            PyObject *rv = PyObject_CallObject(activityRule, activityRuleArgs);
            // rv's type can be obtained with: PyTypeObject* type = rv->ob_type; const char* p = type->tp_name;
            
            if (!rv) {
                PyErr_SetString(PyExc_RuntimeError, "error calling activity_rule");
                return 0;
            }

            if (PyNumber_Check(rv)) {
                PyObject* pyFloat = PyNumber_Float(rv);    
                if (!pyFloat) {
                    PyErr_SetString(PyExc_RuntimeError, "could not convert activity_rule return type to a double");
                    return 0;
                }
                activitiesOverTime[t][c] = PyFloat_AsDouble(pyFloat);
            } else {
                PyErr_SetString(PyExc_RuntimeError, "activity_rule did not return a number");
                return 0;
            }

            // TODO call perturbation rule if exists

            Py_DECREF(neighbourhoodDef);
            Py_DECREF(activities);
            Py_DECREF(cellIndices);
            Py_DECREF(weights);
            Py_DECREF(activityRuleArgs);
            Py_CLEAR(rv);
        }
    }

    Py_DECREF(adjSeq);

    PyObject *finalActivities = buildActivities(activitiesOverTime, timesteps, numCells);

    // free nonZeroIndexMap
    for (unsigned int c = 0; c < numCells; c++) {
        freeList(&nonZeroIndexMap[c]);
    }
    free(nonZeroIndexMap);
    
    // free activitiesOverTime
    for (int i = 0; i < timesteps; i++) {
        free(activitiesOverTime[i]);
    }
    free(activitiesOverTime);
    
    PyObject *ret = PyTuple_New(1);
    PyTuple_SetItem(ret, 0, finalActivities);
    return ret;    
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