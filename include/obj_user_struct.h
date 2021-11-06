#pragma once

typedef struct {
    int id;
    list_int objs_list;
    list_int rec_objs_list;
} user;

typedef struct {
    char name[_BUFFER_SIZE];
    int id;
    double mean_rate;
    unsigned int num_rates;
} obj;
