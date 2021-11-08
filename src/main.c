#include <stdio.h>
#include <stdlib.h> 

// #include "libdtools_consistent.h"
#include "libdtools.h"

int main( int argc, char *argv[] ) {
    if (unlikely(argc != 5)) {
        printf("Not enough arguments\nShould be: users_path objs_path objs_rank_path max_thread_num\n");
        return ERROR_CODE;
    }

    const char *users_path = argv[1];
    const char *objs_path = argv[2];
    const char *objs_rank_path = argv[3];
    const int max_thread_num = atoi( argv[4] );

    // EXAMPLE GENERATION - 1000 objs, 30000 users
    int gen_data_exit_code = __generate_data__(1000, 30000, 500);
    if (unlikely(gen_data_exit_code != 0)) {
        return ERROR_CODE;
    }

    int create_rec_exit_code = timer(create_recomendations, users_path, objs_path, objs_rank_path, 0);
    if (unlikely(create_rec_exit_code != 0)) {
        return ERROR_CODE;
    }

    int create_rec_p_exit_code = timer(create_recomendations_parallel, users_path, objs_path, objs_rank_path, max_thread_num);
    if (unlikely(create_rec_p_exit_code != 0)) {
        return ERROR_CODE;
    }

    return 0;
}
