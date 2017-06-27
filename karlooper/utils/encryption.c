//
// Created by karl on 17-6-23.
//

#include <Python.h>

int length(char *str){
    int i = 0;
    while (str[i] != '\0') i++;
    return i;
}

int flag_func(char *key) {
    int i = 0;
    int flag = 0;
    while (key[i] != '\0') {
        flag += key[i];
        i++;
    }
    return flag % 126;
}

char *str_encrypt(char *input, char *key) {
    int first_length = length(input);
    int second_length = length(key);
    if (second_length == 0 || first_length == 0)
        return input;
    int str_length = first_length + second_length;
    char *result = (char *)PyMem_Malloc((unsigned)(str_length+1));
    int flag = flag_func(key);
    int i;
    for (i = 0; i < first_length; ++i) {
        int encrypt = (int)input[i] + flag;
        if (encrypt > 126) encrypt = encrypt - 126 + 31;
        result[i] = (char)(encrypt);
    }
    int j;
    for (j = first_length; j < str_length; ++j) {
        int encrypt = (int)key[j-first_length] + flag;
        if (encrypt > 126) encrypt = encrypt - 126 + 31;
        result[j] = (char)(encrypt);
    }
    result[str_length] = '\0';
    return result;
}

char *str_decrypt(char *input, char *key) {
    int input_length = length(input);
    int key_length = length(key);
    int flag = flag_func(key);
    int value_length = input_length - key_length;
    char *result = (char *)PyMem_Malloc((unsigned)(value_length+1));
    int i;
    for (i = 0; i < input_length; ++i) {
        int decrypt = (int)input[i] - flag;
        if (decrypt < 32) decrypt = decrypt + 126 - 31;
        result[i] = (char)(decrypt);
    }
    result[value_length] = '\0';
    return result;
}

static PyObject *wrap_encrypt_str(PyObject *self, PyObject *args) {
    char *input_str;
    char *key;
    if (!PyArg_ParseTuple(args, "ss", &input_str, &key)) {
        return NULL;
    }
    char *result = str_encrypt(input_str, key);
    PyObject *pyObject = Py_BuildValue("s", result);
    free(result);
    return pyObject;
}

static PyObject *wrap_decrypt_str(PyObject *self, PyObject *args) {
    char *input_str;
    char *key;
    if (!PyArg_ParseTuple(args, "ss", &input_str, &key)) {
        return NULL;
    }
    char *result = str_decrypt(input_str, key);
    PyObject *obj = Py_BuildValue("s", result);
    free(result);
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
