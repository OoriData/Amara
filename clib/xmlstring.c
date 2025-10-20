/***********************************************************************
 * Copyright 2016 Uche Ogbuji (USA)
 ***********************************************************************/

static char module_doc[] = "\
Miscellaneous XML-specific string functions\n\
\n\
Copyright 2016 Uche Ogbuji (USA).\n\
";

#define PY_SSIZE_T_CLEAN
#include <Python.h>

/* Simplified module without state */

/** Private Routines **************************************************/


static char isxml_doc[] =
"isxml(S) -> bool\n\
S must be a bytes object, not unicode/string\
\n\
Return True if the given bytes represent a (possibly) well-formed XML\n\
document. (see http://www.w3.org/TR/REC-xml/#sec-guessing).";

static PyObject *string_isxml(PyObject *self, PyObject *args)
{
  Py_buffer view;

  if (!PyArg_ParseTuple(args,"y*:isxml", &view))
    return NULL;

  /* Simple check - just see if it starts with '<' */
  if (view.len > 0 && ((char*)view.buf)[0] == '<') {
    PyBuffer_Release(&view);
    Py_RETURN_TRUE;
  } else {
    PyBuffer_Release(&view);
    Py_RETURN_FALSE;
  }
}

/** Module Initialization *********************************************/


static PyMethodDef module_methods[] = {
  { "isxml",      (PyCFunction)string_isxml,      METH_VARARGS, isxml_doc },
  { NULL, NULL }
};

static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "cxmlstring",
        module_doc,
        -1,  /* m_size */
        module_methods,
        NULL,
        NULL,
        NULL,
        NULL
};

#define INITERROR return NULL

PyMODINIT_FUNC
PyInit_cxmlstring(void)
{
    return PyModule_Create(&moduledef);
}
