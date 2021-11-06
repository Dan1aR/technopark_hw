#include <stdlib.h>
#include <stdio.h>
#include <memory.h>
#include <time.h>
#include <dirent.h>

#include "tools.h"
#include "libdataproc.h"

// CONSTS
#define ERROR_CODE -1

const char * _FILES_PATH = "../files/";
const char * _USERS_PATH = "../files/users/";
const char * _OBJS_PATH = "../files/objs/";
const char * _OBJS_RANK_FILE = "../files/objs_rank";
const int _BUFFER_SIZE = 255;


static char* __itoa__(int val, int base) {
	static char buf[32] = {0};
	int i = 30;
	for(; val && i ; --i, val /= base)
		buf[i] = "0123456789abcdef"[val % base];
	return &buf[i+1];
}

static int __generate_objs__(int num_of_objs) {
    srand(time(NULL));
    for (int i = 1; i < num_of_objs; ++i) {
        // Create file_name = _PATH + str(i)
        char *i_buffer = __itoa__(i, 10);
        char *file_name = (char *) malloc(1 + strlen(_OBJS_PATH) + strlen(i_buffer) );
        strcpy(file_name, _OBJS_PATH);
        strcat(file_name, i_buffer);

        FILE * file = fopen( file_name , "wb");
        if (!file) {
            return ERROR_CODE;
        }
        obj *my_obj = (obj*)malloc(sizeof(obj));
        my_obj->name = file_name;
        my_obj->id = i;
        my_obj->mean_rate = ((float)rand()/(float)(RAND_MAX)) * 4 + 1;
        my_obj->num_rates = 1 + i;

        fwrite(my_obj, sizeof(obj), 1, file);
        fclose(file);
    }
    return 0;
}

static int __generate_users__(int num_of_users, int delta) {
    for (int i = 1; i < num_of_users; ++i) {
        // Create file_name = _PATH + str(i)
        char *i_buffer = __itoa__(i, 10);
        char *file_name = (char *) malloc(1 + strlen(_USERS_PATH) + strlen(i_buffer) );
        strcpy(file_name, _USERS_PATH);
        strcat(file_name, i_buffer);

        FILE * file = fopen( file_name , "wb");
        if (!file) {
            return ERROR_CODE;
        }
        user *my_user = (user*)malloc(sizeof(user));
        my_user->id = i;
        list_int obj_list = {NULL, 0};
        for (int j = 0; j < i-delta; ++j) {
            push_back(&obj_list, j);
        }
        my_user->objs_list = obj_list;
        list_int rec_obj_list = {NULL, 0};
        my_user->rec_objs_list = rec_obj_list;

        fwrite(my_user, sizeof(obj), 1, file);
        fclose(file);
    }
    return 0;
}

int __generate_data__(int num_of_objs, int num_of_users, int delta) {
    if (num_of_users < num_of_objs) {
        int objs_exit_code = __generate_objs__(num_of_objs);
        int users_exit_code = __generate_users__(num_of_users, delta);
        if (objs_exit_code == 0 && users_exit_code == 0) {
            return 0;
        }
    }
    return ERROR_CODE;
}

static obj read_obj_from_file(const char *file_name) {
    obj my_obj;
    FILE * file = fopen(file_name, "rb");
    fread(&my_obj, sizeof(obj), 1, file);
    fclose(file);
    return my_obj;
}

static user read_user_from_file(const char *file_name) {
    user my_user;
    FILE * file = fopen(file_name, "rb");
    fread(&my_user, sizeof(user), 1, file);
    fclose(file);
    return my_user;
}

static int write_user_to_file(const user *my_user, const char *file_name) {
    FILE * file = fopen(file_name, "wb");
    if (!file) {
        return ERROR_CODE;
    }
    fwrite(my_user, sizeof(user), 1, file);
    fclose(file);

    return 0;
}

static vector_pairs_int_double get_objs_vector(const char *objs_files_path) {
    vector_pairs_int_double vector = {NULL, 0, 0};
    
    DIR* dir = opendir(objs_files_path);
    struct dirent* entity;
    entity = readdir(dir);
    while (entity != NULL) {
        // .DS_Store protection edded :)
        if ( (entity->d_type != DT_DIR) && (strchr(entity->d_name, '.') == 0) ) {
            char path[100] = { 0 };
            strcat(path, objs_files_path);
            strcat(path, entity->d_name);
            obj my_obj = read_obj_from_file(path);
            pair_int_double pair = {my_obj.id, my_obj.mean_rate};
            push_back_vp(&vector, pair);
        }
        entity = readdir(dir);
    }

    closedir(dir);
    return vector;
}

static int create_objs_rank_file(vector_pairs_int_double *vector, const char * file_name) {
    qsort_pairs(vector, 0, vector->size-1);

    FILE *file = fopen(file_name, "w");
    if (!file) {
        return ERROR_CODE;
    }
    for (int i = 0; i < vector->size; ++i) {
        // printf("%d %f\n", vector.arr[i].first, vector.arr[i].second);
        fprintf(file, "%d %f\n", vector->arr[i].first, vector->arr[i].second);
    }

    fclose(file);
    return 0;
}

static int list_objs_rec_for_user(user *my_user, vector_pairs_int_double *vector) {
    if (!my_user || !vector) {
        return ERROR_CODE;
    }

    list_int rec_objs_list = {NULL, 0};
    int i = 0;
    while (rec_objs_list.size < 10 && i < vector->size) {
        if (!in(&my_user->objs_list, vector->arr[i].first)) {
            push_back(&rec_objs_list, vector->arr[i].first);
            //printf("%d HERE :: %d; Rec-size = %d\n", i, vector->arr[i].first, rec_obj_list.size);
        }
        i++;
    }
    my_user->rec_objs_list = rec_objs_list;
    return 0;
}

int create_recomendations(const char *users_files_path, const char *objs_files_path, const char *objs_rank_file) {
    vector_pairs_int_double vector = get_objs_vector(objs_files_path);
    int rank_file_exit_code = create_objs_rank_file(&vector, objs_rank_file);
    if (rank_file_exit_code == ERROR_CODE) {
        return ERROR_CODE;
    }

    DIR* dir = opendir(users_files_path);
    struct dirent* entity;
    entity = readdir(dir);
    while (entity != NULL) {
        // .DS_Store protection edded :)
        if ( (entity->d_type != DT_DIR) && (strchr(entity->d_name, '.') == 0) ) {
            char path[100] = { 0 };
            strcat(path, users_files_path);
            strcat(path, entity->d_name);
            user my_user = read_user_from_file(path);

            //printf("%s\n", path);
            
            int rec_objs_exit_code = list_objs_rec_for_user(&my_user, &vector);
            if (rec_objs_exit_code == ERROR_CODE) {
                return ERROR_CODE;
            }
            write_user_to_file(&my_user, path);
        }
        entity = readdir(dir);
    }

    closedir(dir);
    return 0;
}
