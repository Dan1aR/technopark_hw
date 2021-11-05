#pragma once

typedef struct sub_my_list_int {
    int val;
    struct sub_my_list_int *next;
} my_list_int;

typedef struct {
    my_list_int *head;
    unsigned int size;
} list_int;

int get(list_int *list, unsigned int i);
int push_back(list_int *list, int val);
