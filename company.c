#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define START_ARRAY_CONST 4

struct Company {
    char *document_type;
    double value;
    char *counterparty_name;
    int day;
    int mounth;
    int year;
    int add_agreements;
    double add_agreements_value;
};

typedef struct Company Cmp_obj;

Cmp_obj Company_new(char *_document_type, double _value, char *_counterparty_name, unsigned int _day, unsigned int _mounth, unsigned int _year, int _add_agreements, double _add_agreements_value) {
    Cmp_obj p;

    p.document_type = (char*)malloc(sizeof(_document_type));
    strcpy(p.document_type, _document_type);

    p.value = _value;

    p.counterparty_name = (char*)malloc(sizeof(_counterparty_name));
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
    p.arr = (Cmp_obj*)malloc(START_ARRAY_CONST * sizeof(Cmp_obj));
    p.buffer_size = START_ARRAY_CONST;
    p.size = 0;
    return p;
}

void clear_array(cmp_obj_array *cmp) {
    free(cmp->arr);
    cmp->arr = NULL;
    cmp->buffer_size = cmp->size = 0;
}

void add_el(cmp_obj_array *cmp ,char *_document_type, double _value, char *_counterparty_name, unsigned int _day, unsigned int _mounth, unsigned int _year, int _add_agreements, double _add_agreements_value) {
    if (cmp->size == cmp->buffer_size) {
        cmp->buffer_size *= 2;
        cmp->arr = (Cmp_obj*)realloc(cmp->arr, cmp->buffer_size * sizeof(Cmp_obj));
    }
    
    cmp->arr[cmp->size++] = Company_new(_document_type, _value, _counterparty_name, _day, _mounth, _year, _add_agreements, _add_agreements_value);
}

static void insert_value_in_max(int *max_idx, double *max_vls, double val, int idx) {
    if (val > max_vls[2]) {
        max_vls[0] = max_vls[1];
        max_idx[0] = max_idx[1];

        max_vls[1] = max_vls[2];
        max_idx[1] = max_idx[2];

        max_vls[2] = val;
        max_idx[2] = idx;
    }
    else if (val > max_vls[1]) {
        max_vls[0] = max_vls[1];
        max_idx[0] = max_idx[1];

        max_vls[1] = val;
        max_idx[1] = idx;
    }
    else if (val > max_vls[0]) {
        max_vls[0] = val;
        max_idx[0] = idx;
    }
}

void find_three_max_counterparty(cmp_obj_array *cmp, int *max_indexes) {
    max_indexes[0] = -1;
    max_indexes[1] = -1;
    max_indexes[2] = -1;
    double max_values[3] = {0, 0, 0};

    for (int i = 0; i < cmp->size; ++i) {
        insert_value_in_max(max_indexes, max_values, cmp->arr[i].value + cmp->arr[i].add_agreements_value, i);
    }
    //printf("%d %d %d \n", max_indexes[0], max_indexes[1], max_indexes[2]);
}

