#include <stdio.h>

// #include "libdtools_consistent.h"
#include "libdtools.h"

int main() {
    // EXAMPLE GENERATION - 1000 objs, 500 users
    // Every user already know about [0 ... 450] objs
    int gen_data_exit_code = __generate_data__(1000, 500, 50);
    if (unlikely(gen_data_exit_code != 0)) {
        return ERROR_CODE;
    }

    int create_rec_exit_code = create_recomendations_parallel("../files/users/", "../files/objs/", "../files/objs_rank");
    if (unlikely(create_rec_exit_code != 0)) {
        return ERROR_CODE;
    }

    user my_user;
    FILE *file = fopen("../files/users/49", "rb");
    fread(&my_user, sizeof(user), 1, file);
    fclose(file);

    printf("%d - %d\n", my_user.id, my_user.rec_objs_list.size);
    for (int i = 0; i < my_user.rec_objs_list.size; ++i) {
        printf("%d ", get(&my_user.rec_objs_list, i));
    }
    printf("\n");

    return 0;
}
