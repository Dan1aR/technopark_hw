#pragma once

#include "tools.h"

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
