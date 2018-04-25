
#include <Python.h>
#include "AX5043_SPI.h"
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

static char module_docstring[] =
    "This module provides an interface for AX5043 Antenna.";

static char ax5043_init_docstring[] = 
    "Inititalize the antenna.";
static char ax5043_write_docstring[] = 
    "Write packets to AX_REG_FIFODATA register.";
static char ax5043_write_reg_docstring[] = 
    "Write packets to the specified register.";
static char ax5043_read_reg_docstring[] = 
    "Read packets from a specified register.";
static char ax5043_set_reg_tx_docstring[] = 
    "Setting up AX5043 to TX mode.";
static char ax5043_set_reg_rx_docstring[] = 
    "Setting up AX5043 to RX mode.";
static char ax5043_write_preamble_docstring[] = 
    "Writing the preamble for transmission";



static PyObject *ax5043_ax5043_init(PyObject *self, PyObject *args);
static PyObject *ax5043_ax5043_write(PyObject *self, PyObject *args);
static PyObject *ax5043_ax5043_write_reg(PyObject *self, PyObject *args);
static PyObject *ax5043_ax5043_read_reg(PyObject *self, PyObject *args);
static PyObject *ax5043_ax5043_set_reg_tx(PyObject *self, PyObject *args);
static PyObject *ax5043_ax5043_set_reg_rx(PyObject *self, PyObject *args);
static PyObject *ax5043_ax5043_write_preamble(PyObject *self, PyObject *args);

static PyMethodDef module_methods[] = {
    {"init", ax5043_ax5043_init, METH_VARARGS, ax5043_init_docstring},
    {"write", ax5043_ax5043_write, METH_VARARGS, ax5043_write_docstring},
    {"write_reg", ax5043_ax5043_write_reg, METH_VARARGS, ax5043_write_reg_docstring},
    {"read_reg", ax5043_ax5043_read_reg, METH_VARARGS, ax5043_read_reg_docstring},
    {"set_reg_tx", ax5043_ax5043_set_reg_tx, METH_VARARGS, ax5043_set_reg_tx_docstring},
    {"set_reg_rx", ax5043_ax5043_set_reg_rx, METH_VARARGS, ax5043_set_reg_rx_docstring},
    {"write_preamble", ax5043_ax5043_write_preamble, METH_VARARGS, ax5043_write_preamble_docstring},
    {NULL, NULL, 0, NULL}
};


PyMODINIT_FUNC PyInit__ax5043(void)
{
    PyObject *module;
    static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "_ax5043",
        module_docstring,
        -1,
        module_methods,
        NULL,
        NULL,
        NULL,
        NULL
    };
    module = PyModule_Create(&moduledef);
    if (!module) return NULL;

    return module;
}

static PyObject *ax5043_ax5043_write(PyObject *self, PyObject *args){
    ax5043_init();
}

static PyObject *ax5043_ax5043_write(PyObject *self, PyObject *args){
    unsigned char value;
     if (!PyArg_ParseTuple(args, "B", &value))
        return NULL;
    ax5043_write(value);

    PyObject *ret = Py_BuildValue("B", value);
    return ret;
}

static PyObject *ax5043_ax5043_write_reg(PyObject *self, PyObject *args){
    uint16_t addr;
    unsigned char value;
     if (!PyArg_ParseTuple(args, "HB",&addr, &value))
        return NULL;
    ax5043_write_reg(addr,value);

    PyObject *ret = Py_BuildValue("B", value);
    return ret;
}

static PyObject *ax5043_ax5043_read_reg(PyObject *self, PyObject *args){
    uint16_t addr;
     if (!PyArg_ParseTuple(args, "H",&addr))
        return NULL;
    char ch = ax5043_read_reg(addr);

    PyObject *ret = Py_BuildValue("c", char);
    return ret;
}

static PyObject *ax5043_ax5043_set_reg_tx(PyObject *self, PyObject *args){
    ax5043_set_reg_tx();
    return NULL;
}

static PyObject *ax5043_ax5043_set_reg_rx(PyObject *self, PyObject *args){
    ax5043_set_reg_rx();
    return NULL;
}

static PyObject *ax5043_ax5043_write_preamble(PyObject *self, PyObject *args){
    ax5043_writePreamble();
    return NULL;
}