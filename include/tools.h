#pragma once

#define unlikely(x) __builtin_expect((x),0)

typedef struct sub_my_list_int {
    int val;
    struct sub_my_list_int *next;
} my_list_int;

typedef struct {
    my_list_int *head;
    unsigned int size;
} list_int;

int get(const list_int *list, unsigned int i);
int push_back(list_int *list, int val);
int in(const list_int *list, int val);

typedef struct {
    int first;
    double second;
} pair_int_double;

typedef struct {
    pair_int_double *arr;
    unsigned int size;
    unsigned int buffer_size;
} vector_pairs_int_double;

int push_back_vp(vector_pairs_int_double *vector, pair_int_double pair);
void swap_pair(pair_int_double *first, pair_int_double *second);
int partition (vector_pairs_int_double *vector, int low, int high);
void qsort_pairs(vector_pairs_int_double *vector, int low, int high);
