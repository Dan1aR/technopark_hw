#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#define START_ARRAY_CONST 4
#define STR_CONST

typedef enum { false, true } bool;

struct Company {
    char *document_type;
    double value;
    char *counterparty_name;
    int day;
    int mounth;
    int year;
    bool add_agreements;
    double add_agreements_value;
};

typedef struct Company Cmp_obj;

Cmp_obj Company_new(char *_document_type, double _value, char *_counterparty_name, unsigned int _day, unsigned int _mounth, unsigned int _year, bool _add_agreements, double _add_agreements_value) {
    Cmp_obj p;
    p.document_type = malloc(sizeof(_document_type));
    strcpy(p.document_type, _document_type);
    p.value = _value;
    p.counterparty_name = malloc(sizeof(_counterparty_name));
    strcpy(p.counterparty_name, _counterparty_name);
    p.day = _day;
    p.mounth = _mounth;
    p.year = -_year;
    p.add_agreements = _add_agreements;
    p.add_agreements_value = _add_agreements_value;
    return p;
}

struct cmp_obj_array_struct {
    Cmp_obj *arr;
    int buffer_size;
    int size;
};

typedef struct cmp_obj_array_struct cmp_obj_array;

cmp_obj_array create_array() {
    cmp_obj_array p;
    p.arr = malloc(START_ARRAY_CONST * sizeof(Cmp_obj));
    p.buffer_size = START_ARRAY_CONST;
    p.size = 0;
    return p;
}

void clear_array(cmp_obj_array *cmp) {
    free(cmp->arr);
    cmp->arr = NULL;
    cmp->buffer_size = cmp->size = 0;
}

void add_el(cmp_obj_array *cmp ,char *_document_type, double _value, char *_counterparty_name, unsigned int _day, unsigned int _mounth, unsigned int _year, bool _add_agreements, double _add_agreements_value) {
    if (cmp->size == cmp->buffer_size) {
        cmp->buffer_size *= 2;
        cmp->arr = realloc(cmp->arr, cmp->buffer_size * sizeof(Cmp_obj));
    }
    
    cmp->arr[cmp->size++] = Company_new(_document_type, _value, _counterparty_name, _day, _mounth, _year, _add_agreements, _add_agreements_value);
}

void show_arr(cmp_obj_array *cmp) {
    printf("Arr::\n");
    for (int i = 0; i < cmp->size; ++i) {
        printf(">>> %s - %f \n", cmp->arr[i].counterparty_name, cmp->arr[i].value);
    }
}

