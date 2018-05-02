#include <Python.h>
#include "AX5043_SPI.h"
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

static char module_docstring[] =
    "This module provides an interface for AX5043 Antenna.";

static char ax5043_init_docstring[] = 
    "Inititalize the antenna.";
static char ax5043_SPI_setup_docstring[] = 
    "Inititalize wiringSPI.";
static char ax5043_write_docstring[] = 
    "Write packets to AX_REG_FIFODATA register.";
static char ax5043_write_reg_docstring[] = 
    "Write packets to the specified register.";
static char ax5043_read_reg_docstring[] = 
    "Read packets from a specified register.";



static PyObject *ax5043_ax5043_init(PyObject *self, PyObject *args);
static PyObject *ax5043_ax5043_SPI_setup(PyObject *self, PyObject *args);
static PyObject *ax5043_ax5043_write(PyObject *self, PyObject *args);
static PyObject *ax5043_ax5043_write_reg(PyObject *self, PyObject *args);
static PyObject *ax5043_ax5043_read_reg(PyObject *self, PyObject *args);

static PyMethodDef module_methods[] = {
    {"init", ax5043_ax5043_init, METH_VARARGS, ax5043_init_docstring},
    {"setup_SPI", ax5043_ax5043_SPI_setup, METH_VARARGS, ax5043_init_docstring},
    {"write", ax5043_ax5043_write, METH_VARARGS, ax5043_write_docstring},
    {"write_reg", ax5043_ax5043_write_reg, METH_VARARGS, ax5043_write_reg_docstring},
    {"read_reg", ax5043_ax5043_read_reg, METH_VARARGS, ax5043_read_reg_docstring},
    {NULL, NULL, 0, NULL}
};


PyMODINIT_FUNC init_ax5043(void)
{
	PyObject *m = Py_InitModule3("_ax5043", module_methods, module_docstring);
	if(m == NULL)
		return;

}

static PyObject *ax5043_ax5043_init(PyObject *self, PyObject *args){
    ax5043_init();
}

static PyObject *ax5043_ax5043_SPI_setup(PyObject *self, PyObject *args){
    char *filename;
    if (!PyArg_ParseTuple(args, "z", &filename))
        return NULL;
    ax5043_SPI_setup(filename);
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
    ax5043_writeReg(addr,value);

    PyObject *ret = Py_BuildValue("B", value);
    return ret;
}

static PyObject *ax5043_ax5043_read_reg(PyObject *self, PyObject *args){
    uint16_t addr;
     if (!PyArg_ParseTuple(args, "H",&addr))
        return NULL;
    char ch = ax5043_readReg(addr);

    PyObject *ret = Py_BuildValue("c", ch);
    return ret;
}

