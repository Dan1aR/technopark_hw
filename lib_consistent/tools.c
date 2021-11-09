#include "tools.h"

#include <stdio.h>
#include <stdlib.h>

// list
void free_list(list_int *list) {
  while (list->head) {
    my_list_int *tmp = list->head;
    list->head = list->head->next;
    free(tmp);
  }
}

int push_back(list_int *list, int val) {
  if (unlikely(!list)) {
    return ERROR_CODE;
  }
  if (!list->head) {
    list->head = (my_list_int *)malloc(sizeof(my_list_int));
    if (unlikely(!list->head)) {
      return ERROR_CODE;
    }
    list->head->next = NULL;
    list->head->val = val;
    list->size = 1;
  } else {
    my_list_int *node = list->head;
    for (int i = 0; i < list->size - 1; ++i) {
      node = node->next;
    }
    node->next = (my_list_int *)malloc(sizeof(my_list_int));
    if (unlikely(!node->next)) {
      return ERROR_CODE;
    }
    node->next->next = NULL;
    node->next->val = val;
    list->size++;
  }
  return 0;
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

// vector

int push_back_vp(vector_pairs_int_double *vector, pair_int_double pair) {
  if (unlikely(!vector)) {
    return ERROR_CODE;
  }
  if (vector->size == vector->buffer_size) {
    vector->buffer_size =
        (vector->buffer_size == 0) ? 2 : vector->buffer_size * 2;
    pair_int_double *tmp = (pair_int_double *)realloc(
        vector->arr, vector->buffer_size * sizeof(pair_int_double));
    if (tmp) {
      vector->arr = tmp;
    } else {
      free(vector->arr);
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

int partition(vector_pairs_int_double *vector, int low, int high) {
  pair_int_double pivot = vector->arr[high];  // pivot
  int i = (low - 1);                          // Index of smaller element

  for (int j = low; j <= high - 1; j++) {
    if (vector->arr[j].second >= pivot.second) {
      i++;  // increment index of smaller element
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

// read write user to file
user read_user_from_file(const char *file_name) {
  // Initialize my_user
  user my_user = {0, {NULL, 0}, {NULL, 0}};

  FILE *file = fopen(file_name, "r");
  if (file) {
    char *line = NULL;
    size_t len = 0;

    getline(&line, &len, file);
    my_user.id = atoi(line);

    getline(&line, &len, file);
    int objs_list_size = atoi(line);
    for (int i = 0; i < objs_list_size; ++i) {
      getline(&line, &len, file);
      int val = atoi(line);
      push_back(&my_user.objs_list, val);
    }
    getline(&line, &len, file);
    int rec_objs_list_size = atoi(line);
    for (int i = 0; i < rec_objs_list_size; ++i) {
      getline(&line, &len, file);
      int val = atoi(line);
      push_back(&my_user.rec_objs_list, val);
    }

    fclose(file);
    if (line) free(line);

    return my_user;
  }
  exit(ERROR_CODE);
}

int write_user_to_file(user *my_user, const char *file_name) {
  FILE *file = fopen(file_name, "w");
  if (file) {
    fprintf(file, "%d\n", my_user->id);
    fprintf(file, "%d\n", my_user->objs_list.size);
    while (my_user->objs_list.head) {
      fprintf(file, "%d\n", my_user->objs_list.head->val);
      my_list_int *tmp = my_user->objs_list.head;
      my_user->objs_list.head = my_user->objs_list.head->next;
      free(tmp);
    }
    fprintf(file, "%d\n", my_user->rec_objs_list.size);
    while (my_user->rec_objs_list.head) {
      fprintf(file, "%d\n", my_user->rec_objs_list.head->val);
      my_list_int *tmp = my_user->rec_objs_list.head;
      my_user->rec_objs_list.head = my_user->rec_objs_list.head->next;
      free(tmp);
    }
    fclose(file);
    return 0;
  }
  return ERROR_CODE;
}
