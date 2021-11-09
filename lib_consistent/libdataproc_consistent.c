#include <dirent.h>
#include <memory.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "libdtools.h"

static obj read_obj_from_file(const char *file_name) {
  obj my_obj;
  FILE *file = fopen(file_name, "rb");
  fread(&my_obj, sizeof(obj), 1, file);
  fclose(file);
  return my_obj;
}

static vector_pairs_int_double get_objs_vector(const char *objs_files_path) {
  vector_pairs_int_double vector = {NULL, 0, 0};

  DIR *dir = opendir(objs_files_path);
  struct dirent *entity;
  entity = readdir(dir);
  while (entity != NULL) {
    // .DS_Store protection edded :)
    if ((entity->d_type != DT_DIR) && (strchr(entity->d_name, '.') == 0)) {
      char path[_BUFFER_SIZE] = {0};
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

static int create_objs_rank_file(vector_pairs_int_double *vector,
                                 const char *file_name) {
  qsort_pairs(vector, 0, vector->size - 1);

  FILE *file = fopen(file_name, "w");
  if (file) {
    for (int i = 0; i < vector->size; ++i) {
      fprintf(file, "%d %f\n", vector->arr[i].first, vector->arr[i].second);
    }

    fclose(file);
    return 0;
  }
  return ERROR_CODE;
}

static int list_objs_rec_for_user(user *my_user,
                                  vector_pairs_int_double *vector) {
  if (unlikely(!my_user || !vector)) {
    return ERROR_CODE;
  }

  list_int rec_objs_list = {NULL, 0};
  int i = 0;
  while (rec_objs_list.size < 10 && i < vector->size) {
    if (!in(&my_user->objs_list, vector->arr[i].first)) {
      push_back(&rec_objs_list, vector->arr[i].first);
      // printf("%d HERE :: %d; Rec-size = %d\n", i, vector->arr[i].first,
      // rec_obj_list.size);
    }
    i++;
  }
  my_user->rec_objs_list = rec_objs_list;
  return 0;
}

int create_recomendations(const char *users_files_path,
                          const char *objs_files_path,
                          const char *objs_rank_file,
                          const int _max_thread_num) {
  if (unlikely(_max_thread_num != 0)) {
    return ERROR_CODE;
  }

  vector_pairs_int_double vector = get_objs_vector(objs_files_path);
  int rank_file_exit_code = create_objs_rank_file(&vector, objs_rank_file);
  if (unlikely(rank_file_exit_code == ERROR_CODE)) {
    return ERROR_CODE;
  }

  DIR *dir = opendir(users_files_path);
  struct dirent *entity;
  entity = readdir(dir);
  while (entity != NULL) {
    // .DS_Store protection edded :)
    if ((entity->d_type != DT_DIR) && (strchr(entity->d_name, '.') == 0)) {
      char path[_BUFFER_SIZE] = {0};
      strcat(path, users_files_path);
      strcat(path, entity->d_name);
      user my_user = read_user_from_file(path);

      int rec_objs_exit_code = list_objs_rec_for_user(&my_user, &vector);
      if (unlikely(rec_objs_exit_code == ERROR_CODE)) {
        return ERROR_CODE;
      }
      write_user_to_file(&my_user, path);
      free_list(&my_user.objs_list);
      free_list(&my_user.rec_objs_list);
    }
    entity = readdir(dir);
  }

  free(vector.arr);
  closedir(dir);
  return 0;
}
