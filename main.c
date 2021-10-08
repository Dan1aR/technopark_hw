#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "company.h"

#define STR_CONST_LEN 25

void ui() {
    printf(">>> 1) Добавить Информацию о договоре\n");
    printf(">>> 2) Три ключевых контрагента\n");
    printf(">>> 0) Выход\n");
    printf(">>> ");
}


void add_info(cmp_obj_array *cmp) {
    char _dc[STR_CONST_LEN];
    printf(">>> Введите тип документа: ");
    scanf("%25s", _dc);

    double _v;
    printf(">>> Введите сумму договора: ");
    scanf("%lf", &_v);

    char _cn[STR_CONST_LEN];
    printf(">>> Введите название контрагента: ");
    scanf("%25s", _cn);

    char _date[STR_CONST_LEN];
    printf(">>> Введите дату в формате день.месяц.год - 6.Dec.2001: ");
    scanf("%25s", _date);
    struct tm tm;
    while (!strptime(_date, "%d.%b.%Y", &tm)) {
        printf(">>> Некорректно введены данные \n");
        printf(">>> Ожидается формат день.месяц.год - 6.Dec.2001 \n >>> ");
        scanf("%25s", _date);
    }

    printf(">>> Есть ли дополнительные соглашения? [1 - да/0 - нет]: ");
    bool _ag;
    scanf("%d", &_ag);
    double _agv = 0;
    if (_ag) {
        printf(">>> Введите сумму дополнительных соглашений: ");
        scanf("%lf", &_agv);
    }

    add_el(cmp, _dc, _v, _cn, tm.tm_mday, tm.tm_mon, tm.tm_year, _ag, _agv);
    //printf("HERE :: %s\n", cmp->arr[cmp->size-1].counterparty_name);
}

int main () {
    
    cmp_obj_array cmp = create_array();

    printf("\t\t\tБаза данных с Информацией о договорах\n");
    int user_command = 1;
    while (user_command) {
        ui();
        scanf("%d", &user_command);
        if (user_command == 1) {
            add_info(&cmp);
            //printf("HERE :: %s - %2f - %d\n", cmp.arr[cmp.size-1].counterparty_name, cmp.arr[cmp.size-1].value, cmp.arr[cmp.size-1].day);
        }
        else if (user_command == 2) {

        }
        else if (user_command == 0) {
            break;
        }
        else {
            printf(">>> Команда не распознана\n");
        }
    }

    show_arr(&cmp);

    clear_array(&cmp);

}