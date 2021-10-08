#pragma once

typedef struct Company Cmp_obj;
typedef enum { false, true } bool;
typedef struct cmp_obj_array_struct cmp_obj_array;

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

Cmp_obj* Company_new(char *, double, char *, bool, double);

struct cmp_obj_array_struct {
    Cmp_obj *arr;
    int buffer_size;
    int size;
};

cmp_obj_array create_array();
void clear_array(cmp_obj_array*);
void add_el(cmp_obj_array* ,char*, double, char*, unsigned int, unsigned int, unsigned int, bool, double);
void show_arr(cmp_obj_array*);
int* find_three_max_counterparty(cmp_obj_array*, int*);

