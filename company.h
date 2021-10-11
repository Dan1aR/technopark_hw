#pragma once

typedef struct {
  char* document_type;
  double value;
  char* counterparty_name;
  int day;
  int mounth;
  int year;
  int add_agreements;
  double add_agreements_value;
} Cmp_obj;

Cmp_obj Company_new(char*, double, char*, unsigned int, unsigned int,
                    unsigned int, int, double);

typedef struct {
  Cmp_obj* arr;
  size_t buffer_size;
  size_t size;
} cmp_obj_array;

cmp_obj_array create_array();
void clear_array(cmp_obj_array*);
int add_el(cmp_obj_array*, char*, double, char*, unsigned int, unsigned int,
           unsigned int, int, double);
// void show_arr(cmp_obj_array*);
void find_three_max_counterparty(cmp_obj_array*, int*);
