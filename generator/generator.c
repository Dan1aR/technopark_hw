#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

#include "libdtools.h"

// CONSTS
const char * _USERS_PATH = "../files/users/";
const char * _OBJS_PATH = "../files/objs/";

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
        char *file_name = (char*)malloc(_BUFFER_SIZE*sizeof(char));
        strcpy(file_name, _OBJS_PATH);
        strcat(file_name, i_buffer);

        FILE * file = fopen( file_name , "wb");
        if (unlikely(!file)) {
            return ERROR_CODE;
        }

        obj *my_obj = (obj*)malloc(sizeof(obj));
        if (unlikely(!my_obj)) {
            return ERROR_CODE;
        }

        my_obj->name = (char*)malloc(_BUFFER_SIZE*sizeof(char));
        strcpy(my_obj->name, file_name);
        my_obj->id = i;
        my_obj->mean_rate = ((float)rand()/(float)(RAND_MAX)) * 4 + 1;
        my_obj->num_rates = 1 + i;

        fwrite(my_obj, sizeof(obj), 1, file);
        fclose(file);

        free(my_obj->name);
        free(file_name);
        free(my_obj);
    }
    return 0;
}

static int __generate_users__(int num_of_objs, int num_of_users, int delta) {
    for (int i = 1; i < num_of_users; ++i) {
        // Create file_name = _PATH + str(i)
        char *i_buffer = __itoa__(i, 10);
        char *file_name = (char*)malloc(_BUFFER_SIZE*sizeof(char));
        strcpy(file_name, _USERS_PATH);
        strcat(file_name, i_buffer);

        FILE * file = fopen( file_name , "wb");
        if (unlikely(!file)) {
            return ERROR_CODE;
        }
        user *my_user = (user*)malloc(sizeof(user));
        if (unlikely(!my_user)) {
            return ERROR_CODE;
        }
        my_user->id = i;
        list_int obj_list = {NULL, 0};
        for (int j = 0; j < num_of_objs-delta; ++j) {
            push_back(&obj_list, j);
        }
        my_user->objs_list = obj_list;
        list_int rec_obj_list = {NULL, 0};
        my_user->rec_objs_list = rec_obj_list;

        fwrite(my_user, sizeof(obj), 1, file);
        fclose(file);

        //free_list(&my_user->objs_list);
        //free_list(&my_user->rec_objs_list);
        free(file_name);
        free(my_user);
    }
    return 0;
}

int __generate_data__(int num_of_objs, int num_of_users, int delta) {
    int objs_exit_code = __generate_objs__(num_of_objs);
    int users_exit_code = __generate_users__(num_of_objs, num_of_users, delta);
    if (objs_exit_code == 0 && users_exit_code == 0) {
        printf("Successfuly generated: %d objs, %d users\n", num_of_objs, num_of_users);
        return 0;
    }
    return ERROR_CODE;
}
