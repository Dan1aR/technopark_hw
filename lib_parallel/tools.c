#include <stdlib.h>
#include <stdio.h>

#include "tools.h"

// list
int get(const list_int *list, unsigned int i) {
    if (unlikely(!list)) {
        return ERROR_CODE;
    }
    if (unlikely(!list->head)) {
        return ERROR_CODE;
    }
    if (unlikely((i < 0) || (i >= list->size))) {
        return ERROR_CODE;
    }

    my_list_int *node = list->head;
    for (int _i = 0; _i < i; ++_i) {
        node = node->next;
    }
    return node->val;
}

int push_back(list_int *list, int val) {
    if (unlikely(!list)) {
        return ERROR_CODE;
    }
    
    if (!list->head) {
        list->head = (my_list_int*)malloc(sizeof(my_list_int));
        if (unlikely(!list->head)) {
            return ERROR_CODE;
        }
        list->head->next = NULL;
        list->head->val = val;
        list->size = 1;
    }
    else {    
        my_list_int *node = list->head;
        for (int i = 0; i < list->size-1; ++i) {
            node = node->next;
        }
        node->next = (my_list_int*)malloc(sizeof(my_list_int));
        if (unlikely(!node->next)) {
            return ERROR_CODE;
        }
        node->next->next = NULL;
        node->next->val = val;
        list->size++;
    }
    return 0;
}

void print_list(const list_int *list) {
    my_list_int *node = list->head;
    while (node) {
        printf("%d ", node->val);
    }
    printf("\n");
}

int in(const list_int *list, int val) {
    if (unlikely(!list)) {
        return 0;
    }

    my_list_int *node = list->head;
    while (node) {
        if (node->val == val) {
            return 1;
        }
        node = node->next;
    }
    return 0;
}

void free_list(list_int *list) {
    my_list_int* tmp;
    while (list->head != NULL)
    {
       tmp = list->head;
       list->head = list->head->next;
       free(tmp);
    }
}

// vector
int push_back_vp(vector_pairs_int_double *vector, pair_int_double pair) {
    if (unlikely(!vector)) {
        return ERROR_CODE;
    }
    if (vector->size == vector->buffer_size) {
        vector->buffer_size = (vector->buffer_size == 0) ? 2 : vector->buffer_size * 2;
        pair_int_double *tmp = (pair_int_double *)realloc(vector->arr, vector->buffer_size * sizeof(pair_int_double));
        if (tmp) {
            vector->arr = tmp;
        } else {
            return ERROR_CODE;
        }
    }
    vector->arr[vector->size] = pair;
    vector->size++;
    return 0;
}

// sort pairs
void swap_pair(pair_int_double *first, pair_int_double *second) {
    if (first && second) {
        pair_int_double tmp = *first;
        *first = *second;
        *second = tmp;
    }
}

int partition (vector_pairs_int_double *vector, int low, int high) {
    pair_int_double pivot = vector->arr[high];    // pivot
    int i = (low - 1);  // Index of smaller element
 
    for (int j = low; j <= high- 1; j++) {
        if (vector->arr[j].second >= pivot.second) {
            i++;    // increment index of smaller element
            swap_pair(&vector->arr[i], &vector->arr[j]);
        }
    }
    swap_pair(&vector->arr[i + 1], &vector->arr[high]);
    return (i + 1);
}

void qsort_pairs(vector_pairs_int_double *vector, int low, int high) {
    if (vector) {
        if (low < high) {
            int pi = partition(vector, low, high);
            qsort_pairs(vector, low, pi - 1);
            qsort_pairs(vector, pi + 1, high);
        }
    }
}
