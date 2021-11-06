#pragma once

typedef struct {
    int id;
    list_int objs_list;
    list_int rec_objs_list;
} user;

typedef struct {
    const char *name;
    int id;
    double mean_rate;
    unsigned int num_rates;
} obj;

int __generate_data__(int num_of_objs, int num_of_users, int delta);
int create_recomendations(const char *users_files_path, const char *objs_files_path, const char *objs_rank_file);
