#pragma once

#include "generator.h"
#include "tools.h"

int create_recomendations(const char *users_files_path,
                          const char *objs_files_path,
                          const char *objs_rank_file,
                          const int _max_thread_num);
int create_recomendations_parallel(const char *users_files_path,
                                   const char *objs_files_path,
                                   const char *objs_rank_file,
                                   const int _max_thread_num);
int timer(int (*func)(const char *users_files_path, const char *objs_files_path,
                      const char *objs_rank_file, const int _max_thread_num),
          const char *users_files_path, const char *objs_files_path,
          const char *objs_rank_file, const int _max_thread_num);
