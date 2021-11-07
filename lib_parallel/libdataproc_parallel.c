#include <stdlib.h>
#include <stdio.h>
#include <memory.h>
#include <time.h>
#include <dirent.h>
#include <pthread.h>

#include "libdtools.h"

#define _NUM_REC_FOR_USER 10

static obj read_obj_from_file(const char *file_name) {
    obj my_obj;
    FILE * file = fopen(file_name, "rb");
    fread(&my_obj, sizeof(obj), 1, file);
    fclose(file);
    return my_obj;
}

static user read_user_from_file(const char *file_name) {
    user my_user;
    FILE *file = fopen(file_name, "rb");
    printf("%s was here\n", file_name);
    fread(&my_user, sizeof(user), 1, file);
    fclose(file);
    return my_user;
}

static int write_user_to_file(const user *my_user, const char *file_name) {
    FILE * file = fopen(file_name, "wb");
    if (file) {
        fwrite(my_user, sizeof(user), 1, file);
        fclose(file);
        return 0;
    }
    return ERROR_CODE;
}

static vector_pairs_int_double get_objs_vector(const char *objs_files_path) {
    vector_pairs_int_double vector = {NULL, 0, 0};
    
    DIR* dir = opendir(objs_files_path);
    struct dirent* entity;
    entity = readdir(dir);
    while (entity != NULL) {
        // .DS_Store protection edded :)
        if ( (entity->d_type != DT_DIR) && (strchr(entity->d_name, '.') == 0) ) {
            char path[_BUFFER_SIZE] = { 0 };
            strncat(path, objs_files_path, strlen(objs_files_path));
            strncat(path, entity->d_name, strlen(entity->d_name));
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
    if (file) {
        for (int i = 0; i < vector->size; ++i) {
            // printf("%d %f\n", vector.arr[i].first, vector.arr[i].second);
            fprintf(file, "%d %f\n", vector->arr[i].first, vector->arr[i].second);
        }

        fclose(file);
        return 0;
    }
    return ERROR_CODE;
}

typedef struct {
    char my_user_path[_BUFFER_SIZE];
    vector_pairs_int_double *vector;
} args_struct;

void *list_objs_rec_for_user(void *args) {
    if (unlikely(!args)) {
        pthread_exit((void*)ERROR_CODE);
    } 
    int errflag = pthread_detach(pthread_self());
    if (unlikely(errflag != 0)) {
        pthread_exit((void*)ERROR_CODE);
    }
    
    args_struct *arg = (args_struct*)args;
    printf("file path in thread: %s\n", arg->my_user_path);
    printf("vector size in thread = %d\n", arg->vector==NULL );
    user my_user = read_user_from_file( arg->my_user_path );

    list_int rec_objs_list = {NULL, 0};
    int i = 0;
    while ( (rec_objs_list.size < _NUM_REC_FOR_USER) && (i < arg->vector->size) ) {
        if (!in(&my_user.objs_list, arg->vector->arr[i].first)) {
            push_back(&rec_objs_list, arg->vector->arr[i].first);
        }
        i++;
    }

    my_user.rec_objs_list = rec_objs_list;
    write_user_to_file(&my_user, arg->my_user_path);

    pthread_exit(NULL);
}

int create_recomendations_parallel(const char *users_files_path, const char *objs_files_path, const char *objs_rank_file) {
    vector_pairs_int_double vector = get_objs_vector(objs_files_path);
    int rank_file_exit_code = create_objs_rank_file(&vector, objs_rank_file);
    if (unlikely(rank_file_exit_code == ERROR_CODE)) {
        return ERROR_CODE;
    }

    DIR* dir = opendir(users_files_path);
    struct dirent* entity;
    entity = readdir(dir);
    while (entity != NULL) {
        // .DS_Store protection edded :)
        if ( (entity->d_type != DT_DIR) && (strchr(entity->d_name, '.') == 0) ) {
            char path[_BUFFER_SIZE] = { 0 };
            strcat(path, users_files_path);
            strcat(path, entity->d_name);

            pthread_t thread;

            args_struct *args = (args_struct*)malloc(sizeof(args_struct));
            strcpy(args->my_user_path, path);
            args->vector = &vector;

            printf("%s; vector size out of thread = %d\n", args->my_user_path, args->vector->size);
            int rec_objs_exit_code = pthread_create(&thread, NULL, list_objs_rec_for_user, &args);
            if (unlikely(rec_objs_exit_code == ERROR_CODE)) {
                return ERROR_CODE;
            }          
        }
        entity = readdir(dir);
    }

    closedir(dir);

    return 0;
}

