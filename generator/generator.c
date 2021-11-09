#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "libdtools.h"

static char *__itoa__(int val, const int base) {
  static char buf[32] = {0};
  int i = 30;
  for (; val && i; --i, val /= base) buf[i] = "0123456789abcdef"[val % base];
  return &buf[i + 1];
}

static int __generate_objs__(const int num_of_objs, const char *objs_path) {
  srand(time(NULL));
  for (int i = 1; i < num_of_objs; ++i) {
    // Create file_name = _PATH + str(i)
    char *i_buffer = __itoa__(i, 10);
    char *file_name = (char *)malloc(_BUFFER_SIZE * sizeof(char));
    strcpy(file_name, objs_path);
    strcat(file_name, i_buffer);

    FILE *file = fopen(file_name, "wb");
    if (file) {
      obj *my_obj = (obj *)malloc(sizeof(obj));
      memset(my_obj, 0, sizeof(obj));
      if (unlikely(!my_obj)) {
        return ERROR_CODE;
      }

      my_obj->name = (char *)malloc(_BUFFER_SIZE * sizeof(char));
      strcpy(my_obj->name, file_name);
      my_obj->id = i;
      my_obj->mean_rate = ((float)rand() / (float)(RAND_MAX)) * 4 + 1;
      my_obj->num_rates = 1 + i;

      fwrite(my_obj, sizeof(obj), 1, file);
      fclose(file);

      free(my_obj->name);
      free(file_name);
      free(my_obj);
    } else {
      return ERROR_CODE;
    }
  }
  return 0;
}

static int __generate_users__(const int num_of_objs, const int num_of_users,
                              const int delta, const char *users_path) {
  for (int i = 1; i < num_of_users; ++i) {
    // Create file_name = _PATH + str(i)
    char *i_buffer = __itoa__(i, 10);
    char *file_name = (char *)malloc(_BUFFER_SIZE * sizeof(char));
    strcpy(file_name, users_path);
    strcat(file_name, i_buffer);

    user *my_user = (user *)malloc(sizeof(user));
    memset(my_user, 0, sizeof(user));
    if (unlikely(!my_user)) {
      free(file_name);
      return ERROR_CODE;
    }

    my_user->id = i;
    list_int obj_list = {NULL, 0};
    for (int j = 0; j < num_of_objs - delta; ++j) {
      push_back(&obj_list, j);
    }
    my_user->objs_list = obj_list;
    list_int rec_obj_list = {NULL, 0};
    my_user->rec_objs_list = rec_obj_list;

    write_user_to_file(my_user, file_name);

    // free_list(&my_user->objs_list);
    // free_list(&my_user->rec_objs_list);
    free(file_name);
    free(my_user);
  }
  return 0;
}

int __generate_data__(const int num_of_objs, const int num_of_users,
                      const int delta, const char *users_path,
                      const char *objs_path) {
  int objs_exit_code = __generate_objs__(num_of_objs, objs_path);
  int users_exit_code =
      __generate_users__(num_of_objs, num_of_users, delta, users_path);
  if (objs_exit_code == 0 && users_exit_code == 0) {
    printf("Successfuly generated: %d objs, %d users\n", num_of_objs,
           num_of_users);
    return 0;
  }
  return ERROR_CODE;
}

int __clean_users__(const char *users_path) {
  DIR *dir = opendir(users_path);
  struct dirent *entity;
  entity = readdir(dir);
  while (entity != NULL) {
    // .DS_Store protection edded :)
    if ((entity->d_type != DT_DIR) && (strchr(entity->d_name, '.') == 0)) {
      char path[_BUFFER_SIZE] = {0};
      strcat(path, users_path);
      strcat(path, entity->d_name);
      int rem_exit_code = remove(path);
      if (unlikely(rem_exit_code != 0)) {
        return ERROR_CODE;
      }
    }
    entity = readdir(dir);
  }
  closedir(dir);
  return 0;
}

int __clean_objs__(const char *objs_path) {
  DIR *dir = opendir(objs_path);
  struct dirent *entity;
  entity = readdir(dir);
  while (entity != NULL) {
    // .DS_Store protection edded :)
    if ((entity->d_type != DT_DIR) && (strchr(entity->d_name, '.') == 0)) {
      char path[_BUFFER_SIZE] = {0};
      strcat(path, objs_path);
      strcat(path, entity->d_name);
      int rem_exit_code = remove(path);
      if (unlikely(rem_exit_code != 0)) {
        return ERROR_CODE;
      }
    }
    entity = readdir(dir);
  }
  closedir(dir);
  return 0;
}

int __clean_up__(const char *users_path, const char *objs_path) {
  int clean_users_exit_code = __clean_users__(users_path);
  int clean_objs_exit_code = __clean_objs__(objs_path);
  if (clean_users_exit_code == 0 && clean_objs_exit_code == 0) {
    return 0;
  }
  return ERROR_CODE;
}
