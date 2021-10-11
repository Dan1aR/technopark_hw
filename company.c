#include "company.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define START_ARRAY_CONST 4
#define ERROR_CODE -1
#define MAX_IDX_SIZE 3

Cmp_obj Company_new(char* _document_type, double _value,
                    char* _counterparty_name, unsigned int _day,
                    unsigned int _mounth, unsigned int _year,
                    int _add_agreements, double _add_agreements_value) {
  Cmp_obj p;

  p.document_type = (char*)malloc(sizeof(_document_type));
  if (!p.document_type) {
    printf("malloc return NULL\n");
  }
  strcpy(p.document_type, _document_type);

  p.value = _value;

  p.counterparty_name = (char*)malloc(sizeof(_counterparty_name));
  if (!p.counterparty_name) {
    printf("malloc return NULL\n");
  }
  strcpy(p.counterparty_name, _counterparty_name);

  p.day = _day;
  p.mounth = _mounth;
  p.year = -_year;

  p.add_agreements = _add_agreements;
  p.add_agreements_value = _add_agreements_value;

  return p;
}

cmp_obj_array create_array() {
  cmp_obj_array p;
  p.arr = (Cmp_obj*)malloc(START_ARRAY_CONST * sizeof(Cmp_obj));
  p.buffer_size = (p.arr) ? START_ARRAY_CONST : 0;
  p.size = 0;
  return p;
}

void clear_array(cmp_obj_array* cmp) {
  free(cmp->arr);
  cmp->arr = NULL;
  cmp->buffer_size = cmp->size = 0;
}

int add_el(cmp_obj_array* cmp, char* _document_type, double _value,
           char* _counterparty_name, unsigned int _day, unsigned int _mounth,
           unsigned int _year, int _add_agreements,
           double _add_agreements_value) {
  if (cmp->size == cmp->buffer_size) {
    cmp->buffer_size *= 2;
    Cmp_obj* tmp =
        (Cmp_obj*)realloc(cmp->arr, cmp->buffer_size * sizeof(Cmp_obj));
    if (tmp) {
      cmp->arr = tmp;
    } else {
      return ERROR_CODE;
    }
  }

  cmp->arr[cmp->size] =
      Company_new(_document_type, _value, _counterparty_name, _day, _mounth,
                  _year, _add_agreements, _add_agreements_value);
  // malloc returns NULL check
  if (!cmp->arr[cmp->size].document_type ||
      !cmp->arr[cmp->size].counterparty_name) {
    return ERROR_CODE;
  }

  cmp->size++;
  return 0;
}

static void insert_value_in_max(int* max_idx, double* max_vls, double val,
                                int idx) {
  if (val > max_vls[2]) {
    max_vls[0] = max_vls[1];
    max_idx[0] = max_idx[1];

    max_vls[1] = max_vls[2];
    max_idx[1] = max_idx[2];

    max_vls[2] = val;
    max_idx[2] = idx;
  } else if (val > max_vls[1]) {
    max_vls[0] = max_vls[1];
    max_idx[0] = max_idx[1];

    max_vls[1] = val;
    max_idx[1] = idx;
  } else if (val > max_vls[0]) {
    max_vls[0] = val;
    max_idx[0] = idx;
  }
}

void find_three_max_counterparty(cmp_obj_array* cmp, int* max_indexes) {
  double max_values[MAX_IDX_SIZE];
  for (int i = 0; i < MAX_IDX_SIZE; ++i) {
    max_indexes[i] = -1;
    max_values[i] = 0;
  }

  for (size_t i = 0; i < cmp->size; ++i) {
    insert_value_in_max(max_indexes, max_values,
                        cmp->arr[i].value + cmp->arr[i].add_agreements_value,
                        i);
  }
  // printf("%d %d %d \n", max_indexes[0], max_indexes[1], max_indexes[2]);
}
