#pragma once

#define _BUFFER_SIZE 254
#define ERROR_CODE -1
#define unlikely(x) __builtin_expect((x), 0)

typedef struct sub_my_list_int {
  int val;
  struct sub_my_list_int *next;
} my_list_int;

typedef struct {
  my_list_int *head;
  unsigned int size;
} list_int;

int push_back(list_int *list, int val);
int in(const list_int *list, int val);
void free_list(list_int *list);

typedef struct {
  int first;
  double second;
} pair_int_double;

typedef struct {
  pair_int_double *arr;
  unsigned int size;
  unsigned int buffer_size;
} vector_pairs_int_double;

typedef struct {
  int id;
  list_int objs_list;
  list_int rec_objs_list;
} user;

typedef struct {
  char *name;
  int id;
  double mean_rate;
  unsigned int num_rates;
} obj;

int push_back_vp(vector_pairs_int_double *vector, pair_int_double pair);
void swap_pair(pair_int_double *first, pair_int_double *second);

int partition(vector_pairs_int_double *vector, int low, int high);
void qsort_pairs(vector_pairs_int_double *vector, int low, int high);

user read_user_from_file(const char *file_name);
int write_user_to_file(user *my_user, const char *file_name);
