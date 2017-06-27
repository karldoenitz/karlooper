//
// Created by karl on 17-6-23.
//

#include <Python.h>

static const char *codes = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

static const unsigned char map[256] = {
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 253, 255,
        255, 253, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 253, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255,  62, 255, 255, 255,  63,
        52,  53,  54,  55,  56,  57,  58,  59,  60,  61, 255, 255,
        255, 254, 255, 255, 255,   0,   1,   2,   3,   4,   5,   6,
        7,   8,   9,  10,  11,  12,  13,  14,  15,  16,  17,  18,
        19,  20,  21,  22,  23,  24,  25, 255, 255, 255, 255, 255,
        255,  26,  27,  28,  29,  30,  31,  32,  33,  34,  35,  36,
        37,  38,  39,  40,  41,  42,  43,  44,  45,  46,  47,  48,
        49,  50,  51, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 255
};

int length(char *str){
    int i = 0;
    while (str[i] != '\0') i++;
    return i;
}

char *str_encrypt(char *in) {
    unsigned long len = (unsigned long)length(in);
    unsigned long index, l_even;
    char *p;
//    char *out = (char *) PyMem_Malloc (len * 4 / 3 + 1);
    char *out = (char *) PyMem_Malloc (len * 2);
    p = out;
    /* valid output size ? */
    l_even = 3 * (len / 3);
    for (index = 0; index < l_even; index += 3) {
        *p++ = codes[in[0] >> 2];
        *p++ = codes[((in[0] & 3) << 4) + (in[1] >> 4)];
        *p++ = codes[((in[1] & 0xf) << 2) + (in[2] >> 6)];
        *p++ = codes[in[2] & 0x3f];
        in += 3;
    }
    /* Pad it if necessary...  */
    if (index < len) {
        unsigned a = (unsigned)in[0];
        unsigned b = (unsigned)((index+1 < len) ? in[1] : 0);
        unsigned c = 0;
        *p++ = codes[a >> 2];
        *p++ = codes[((a & 3) << 4) + (b >> 4)];
        *p++ = (char)((index+1 < len) ? codes[((b & 0xf) << 2) + (c >> 6)] : '=');
        *p++ = '=';
    }
    /* append a NULL byte */
    *p = '\0';
    return out;
}

char *str_decrypt(char *in) {
    unsigned long len = (unsigned long)length(in);
//    char *out = (char *) PyMem_Malloc ((len - 1) * 3 / 4);
    char *out = (char *) PyMem_Malloc (len);
    int t, x, y, z;
    unsigned char c;
    int	g = 3;
    for (x = y = z = t = 0; in[x]!=0;) {
        c = map[in[x++]];
        if (c == 255) break;
        if (c == 253) continue;
        if (c == 254) { c = 0; g--; }
        t = (t<<6)|c;
        if (++y == 4) {
            out[z++] = (unsigned char)((t>>16)&255);
            if (g > 1) out[z++] = (unsigned char)((t>>8)&255);
            if (g > 2) out[z++] = (unsigned char)(t&255);
            y = t = 0;
        }
    }
    out[z] = '\0';
    return out;
}

static PyObject *wrap_encrypt_str(PyObject *self, PyObject *args) {
    char *input_str;
    if (!PyArg_ParseTuple(args, "s", &input_str)) {
        return NULL;
    }
    char *result = str_encrypt(input_str);
    PyObject *pyObject = Py_BuildValue("s", result);
    PyMem_Free(result);
    return pyObject;
}

static PyObject *wrap_decrypt_str(PyObject *self, PyObject *args) {
    char *input_str;
    if (!PyArg_ParseTuple(args, "s", &input_str)) {
        return NULL;
    }
    char *result = str_decrypt(input_str);
    PyObject *obj = Py_BuildValue("s", result);
    PyMem_Free(result);
    return obj;
}

/* registration table  */
static PyMethodDef wrap_methods[] ={
        {"encrypt_str", wrap_encrypt_str, METH_VARARGS},       /* method name, C func ptr, always-tuple */
        {"decrypt_str", wrap_decrypt_str, METH_VARARGS},       /* method name, C func ptr, always-tuple */
        {NULL, NULL}                   /* end of table marker */
};

/* module initializer */
PyMODINIT_FUNC initencryption(void)                       /* called on first import */
{                                      /* name matters if loaded dynamically */
    (void)Py_InitModule("encryption", wrap_methods);   /* mod name, table ptr */
}
