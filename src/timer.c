#include <time.h>
#include <stdio.h>

#include "libdtools.h"

int timer(int (*func)(const char *users_files_path, const char *objs_files_path, const char *objs_rank_file, const int _max_thread_num), const char *users_files_path, const char *objs_files_path, const char *objs_rank_file, const int _max_thread_num) {
    if (unlikely(!func)) {
        return ERROR_CODE;
    }

    clock_t start, stop;

    if (_max_thread_num == 0) {
        start = clock();
        int create_rec_exit_code = func(users_files_path, objs_files_path, objs_rank_file, 0);
        if (unlikely(create_rec_exit_code != 0)) {
            return ERROR_CODE;
        }
        
        stop = clock();
        double time = (double)(stop - start) / CLOCKS_PER_SEC;
        printf("RUNTIME FOR CONSISTENT VERSION :: %lfs\n", time);
    }

    if (_max_thread_num > 0) {
        struct timespec start, finish;
        double elapsed;

        clock_gettime(CLOCK_MONOTONIC, &start);
        int create_rec_exit_code = func(users_files_path, objs_files_path, objs_rank_file, _max_thread_num);
        if (unlikely(create_rec_exit_code != 0)) {
            return ERROR_CODE;
        }

        clock_gettime(CLOCK_MONOTONIC, &finish);
        elapsed = (finish.tv_sec - start.tv_sec) + (finish.tv_nsec - start.tv_nsec) / 1000000000.0;
        printf("RUNTIME FOR PARALLEL VERSION :: %lfs\n", elapsed);
    }

    return 0;
}
