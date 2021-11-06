#include <stdio.h>

#include "libdata_tools.h"

int main() {
    __generate_data__(1000, 500, 10);

    create_recomendations("../files/users/", "../files/objs/", "../files/objs_rank");

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
