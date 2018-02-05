/*****************************************************************************
 * Copyright 2015 SoundHound, Incorporated.  All rights reserved.
 *****************************************************************************/
#include <Python.h>

#define SPEEX_HDR_SIZE		80

int SH_speex_init(int quality, char *buffer, int isNB, int buflen);
int SH_speex_encode_frame(short *sFrame, char *cbits);

#if PY_MAJOR_VERSION >= 3
#define FORMAT_RO "y#"
#define FORMAT_S "y#"
#else 
#define FORMAT_RO "t#"
#define FORMAT_S "s#"
#endif

static PyObject *
pySHSpeex_SpeexInit(PyObject *self, PyObject *args)
{
	char buffer[SPEEX_HDR_SIZE];
	int isNB;

	if (!PyArg_ParseTuple(args, "i", &isNB)) {
		return NULL;
	}
	SH_speex_init(10, buffer, isNB, SPEEX_HDR_SIZE);

	return Py_BuildValue(FORMAT_S, buffer, SPEEX_HDR_SIZE);
}

static PyObject *
pySHSpeex_SpeexEncodeFrame(PyObject *self, PyObject *args)
{
	const char *data;
	int len = 0;
	int nbytes = 0;
	char bitsOut[202];

	if (!PyArg_ParseTuple(args, FORMAT_RO, &data, &len)) {
		return NULL;
	}

	nbytes = SH_speex_encode_frame((short*)data, bitsOut);
	return Py_BuildValue(FORMAT_S, bitsOut, nbytes + 2);
}


static PyMethodDef pySHSpeexMethods[] = {
	{ "Init",	pySHSpeex_SpeexInit,	METH_VARARGS,	"Initialize speex codec and return the header bytes." },
	{ "EncodeFrame",	pySHSpeex_SpeexEncodeFrame,	METH_VARARGS,	"Encode one speex frame (320 samples) of 16-khz 16-bit audio." },
	{ NULL, NULL, 0, NULL }
};



#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "pySHSpeex",
        NULL,
        -1,
        pySHSpeexMethods,
        NULL,
        NULL,
        NULL,
        NULL
};

PyMODINIT_FUNC
PyInit_pySHSpeex(void)
{
	PyObject *module = PyModule_Create(&moduledef);
	return module;
}

#else

PyMODINIT_FUNC
initpySHSpeex(void)
{
	(void)Py_InitModule("pySHSpeex", pySHSpeexMethods);
}

#endif
