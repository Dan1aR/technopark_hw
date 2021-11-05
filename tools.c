#include <stdlib.h>
#include <stdio.h>

#include "tools.h"

int get(list_int *list, unsigned int i) {
    if (!list) {
        return -1;
    }
    if ((i < 0) || (i >= list->size)) {
        return -1;
    }

    my_list_int *node = list->head;
    for (int _i = 0; _i < i; ++_i) {
        node = node->next;
    }
    return node->val;
}

int push_back(list_int *list, int val) {
    if (!list) {
        return -1;
    }
    
    if (list->size == 0) {
        list->head = (my_list_int*)malloc(sizeof(my_list_int));
        if (!list->head) {
            return -1;
        }
        list->head->val = val;
        list->size++;
    }
    else {    
        my_list_int *node = list->head;
        for (int i = 0; i < list->size-1; ++i) {
            node = node->next;
        }
        node->next = (my_list_int*)malloc(sizeof(my_list_int));
        if (!node->next) {
            return -1;
        }
        node->next->val = val;
        list->size++;
    }
    return 0;
}
