#define _XOPEN_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "company.h"

#define STR_CONST_LEN 255
#define ERROR_CODE -1

void ui() {
  printf("-----------------------------------\n");
  printf(">>> 1) Добавить Информацию о договоре\n");
  printf(">>> 2) Три ключевых контрагента\n");
  printf(">>> 0) Выход\n");
  printf(">>> ");
}

int add_info(cmp_obj_array* cmp) {
  char _dc[STR_CONST_LEN];
  printf(">>> Введите тип документа: ");
  scanf("%254s", _dc);

  double _v;
  printf(">>> Введите сумму договора: ");
  scanf("%lf", &_v);

  char _cn[STR_CONST_LEN];
  printf(">>> Введите название контрагента: ");
  scanf("%254s", _cn);

  char _date[STR_CONST_LEN];
  printf(">>> Введите дату в формате день.месяц.год - 6.Dec.2001: ");
  scanf("%254s", _date);
  struct tm _tm;
  while (!strptime(_date, "%d.%b.%Y", &_tm)) {
    printf(">>> Некорректно введены данные \n");
    printf(">>> Ожидается формат день.месяц.год - 6.Dec.2001 \n >>> ");
    scanf("%254s", _date);
  }

  printf(">>> Есть ли дополнительные соглашения? [1 - да/0 - нет]: ");
  int _ag;
  scanf("%d", &_ag);
  double _agv = 0;
  if (_ag) {
    printf(">>> Введите сумму дополнительных соглашений: ");
    scanf("%lf", &_agv);
  }

  return add_el(cmp, _dc, _v, _cn, _tm.tm_mday, _tm.tm_mon, _tm.tm_year, _ag,
                _agv);
}

int show_three_max_counterparty(cmp_obj_array* cmp) {
  const int max_idx_size = 3;
  int* max_idx = (int*)malloc(max_idx_size * sizeof(int));
  if (!max_idx) {
    printf("malloc return NULL\n");
    free(max_idx);
    return ERROR_CODE;
  }
  find_three_max_counterparty(cmp, max_idx);

  printf("Самые ценные контрагенты:\n");
  printf("Имя - Сумма Договора - Сумма Дополнительных соглашений\n");
  for (int _idx = 2; _idx >= 0; _idx--) {
    if (max_idx[_idx] != -1) {
      printf("%s - %2f - %2f \n", cmp->arr[max_idx[_idx]]->counterparty_name,
             cmp->arr[max_idx[_idx]]->value,
             cmp->arr[max_idx[_idx]]->add_agreements_value);
    }
  }
  free(max_idx);
  return 0;
}

int interract(int user_command, cmp_obj_array* cmp) {
  if (user_command == 1) {
    int exit_code = add_info(cmp);
    if (exit_code == ERROR_CODE) {
      return ERROR_CODE;
    }
  } else if (user_command == 2) {
    int exit_code = show_three_max_counterparty(cmp);
    if (exit_code == ERROR_CODE) {
      return ERROR_CODE;
    }
  } else if (user_command == 0) {
    return 0;
  } else {
    printf(">>> Команда не распознана\n");
  }
  return 1;
}

int main() {
  cmp_obj_array cmp = create_array();
  if (cmp.buffer_size == 0) {
    printf("malloc return NULL\n");
    return ERROR_CODE;
  }

  printf("\t\t\tБаза данных с Информацией о договорах\n");
  int user_command = 1;

  while (user_command) {
    ui();
    scanf("%d", &user_command);
    int exit_code = interract(user_command, &cmp);
    if (exit_code == ERROR_CODE) {
      clear_array(&cmp);
      return exit_code;
    }
  }

  clear_array(&cmp);
  return 0;
}
