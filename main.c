#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "company.h"

#define STR_CONST_LEN 255

void ui() {
    printf("-----------------------------------\n");
    printf(">>> 1) Добавить Информацию о договоре\n");
    printf(">>> 2) Три ключевых контрагента\n");
    printf(">>> 0) Выход\n");
    printf(">>> ");
}


void add_info(cmp_obj_array *cmp) {
    char _dc[STR_CONST_LEN];
    printf(">>> Введите тип документа: ");
    scanf("%255s", _dc);

    double _v;
    printf(">>> Введите сумму договора: ");
    scanf("%lf", &_v);

    char _cn[STR_CONST_LEN];
    printf(">>> Введите название контрагента: ");
    scanf("%255s", _cn);

    char _date[STR_CONST_LEN];
    printf(">>> Введите дату в формате день.месяц.год - 6.Dec.2001: ");
    scanf("%255s", _date);
    struct tm tm;
    while (!strptime(_date, "%d.%b.%Y", &tm)) {
        printf(">>> Некорректно введены данные \n");
        printf(">>> Ожидается формат день.месяц.год - 6.Dec.2001 \n >>> ");
        scanf("%255s", _date);
    }

    printf(">>> Есть ли дополнительные соглашения? [1 - да/0 - нет]: ");
    int _ag;
    scanf("%d", &_ag);
    double _agv = 0;
    if (_ag) {
        printf(">>> Введите сумму дополнительных соглашений: ");
        scanf("%lf", &_agv);
    }

    add_el(cmp, _dc, _v, _cn, tm.tm_mday, tm.tm_mon, tm.tm_year, _ag, _agv);
    //printf("HERE :: %s\n", cmp->arr[cmp->size-1].counterparty_name);
}

int interract(int user_command, cmp_obj_array *cmp) {
    if (user_command == 1) {
        add_info(cmp);
        //printf("HERE :: %s - %2f - %d\n", cmp.arr[cmp.size-1].counterparty_name, cmp.arr[cmp.size-1].value, cmp.arr[cmp.size-1].day);
    }
    else if (user_command == 2) {
        int *max_idx = (int*)malloc(3*sizeof(int));
        find_three_max_counterparty(cmp, max_idx);
        //printf("1) %d %d %d\n", max_idx[0], max_idx[1], max_idx[2]);
        
        printf("Самые ценные контрагенты:\n");
        printf("Имя - Сумма Договора - Сумма Дополнительных соглашений\n");
        if (max_idx[2] != -1) {
            printf("%s - %2f - %2f \n", cmp->arr[max_idx[2]].counterparty_name, cmp->arr[max_idx[2]].value, cmp->arr[max_idx[2]].add_agreements_value);
        }
        if (max_idx[1] != -1) {
            //printf("2) %d %d %d\n", max_idx[0], max_idx[1], max_idx[2]);
            //printf("HERE\n");
            printf("%s - %2f - %2f \n", cmp->arr[max_idx[1]].counterparty_name, cmp->arr[max_idx[1]].value, cmp->arr[max_idx[1]].add_agreements_value);
        }
        if (max_idx[0] != -1) {
            printf("%s - %2f - %2f \n", cmp->arr[max_idx[0]].counterparty_name, cmp->arr[max_idx[0]].value, cmp->arr[max_idx[0]].add_agreements_value);
        }
        
        free(max_idx);
    }
    else if (user_command == 0) {
        return 0;;
    }
    else {
        printf(">>> Команда не распознана\n");
    }
    return 1;
}

int main () {

    cmp_obj_array cmp = create_array();

    printf("\t\t\tБаза данных с Информацией о договорах\n");
    int user_command = 1;
    
    while (user_command) {
        ui();
        scanf("%d", &user_command);
        if (!interract(user_command, &cmp))
            break;
    }

    clear_array(&cmp);
       
}