#include <gtest/gtest.h>
#include <string>
#include <stdio.h>

#include "company.c"


TEST(COMPANY_TEST, Assert_1) {
    cmp_obj_array cmp = create_array();
    EXPECT_EQ(cmp.size, 0);
    EXPECT_EQ(cmp.buffer_size, 4);
}

TEST(COMPANY_TEST, Assert_2) {
    cmp_obj_array cmp = create_array();
    char tp[3] = "t1";
    char nm[3] = "n1";
    add_el(&cmp, tp, 123, nm, 6, 12, 2001, 0, 0);
    EXPECT_EQ(cmp.size, 1);
}

TEST(COMPANY_TEST, Assert_3) {
    cmp_obj_array cmp = create_array();
    char tp[3] = "t1";
    char nm[3] = "n1";

    for (int i = 0; i < 5; ++i)
        add_el(&cmp, tp, 123, nm, 6, 12, 2001, 0, 0);

    EXPECT_EQ(cmp.size, 5);
    EXPECT_EQ(cmp.buffer_size, 8);
}

TEST(COMPANY_TEST, Assert_4) {
    cmp_obj_array cmp = create_array();
    char tp[3] = "t1";
    char nm[3] = "n1";

    add_el(&cmp, tp, 125, nm, 6, 12, 2001, 0, 0);
    add_el(&cmp, tp, 123, nm, 6, 12, 2001, 0, 0);
    add_el(&cmp, tp, 105, nm, 6, 12, 2001, 0, 0);
    add_el(&cmp, tp, 104, nm, 6, 12, 2001, 0, 0);
    int ans[3] = {2, 1, 0};

    int mx[3] = {-1, -1, -1};
    find_three_max_counterparty(&cmp, mx);

    EXPECT_TRUE( 0 == std::memcmp( mx, ans, sizeof( ans ) ) );
}

TEST(COMPANY_TEST, Assert_5) {
    cmp_obj_array cmp = create_array();
    char tp[3] = "t1";
    char nm[3] = "n1";
    add_el(&cmp, tp, 123, nm, 6, 12, 2001, 0, 0);
    clear_array(&cmp);
    EXPECT_EQ(cmp.arr, nullptr);
}

/*
TEST(MAIN_TEST, Asser_6) {
    ::testing::internal::CaptureStdout();

    cmp_obj_array cmp = create_array();
    char tp[3] = "t1";
    char nm[3] = "n1";

    add_el(&cmp, tp, 125, nm, 6, 12, 2001, 0, 0);
    add_el(&cmp, tp, 123, nm, 6, 12, 2001, 0, 0);
    add_el(&cmp, tp, 105, nm, 6, 12, 2001, 0, 0);

    ASSERT_DEATH(interract(2, &cmp), "");
    std::string capturedStdout = ::testing::internal::GetCapturedStdout().c_str();

    std::string ans = std::string("Самые ценные контрагенты:\n") + \
        std::string("Имя - Сумма Договора - Сумма Дополнительных соглашений\n") + \
        std::string(nm) + std::string(" - 125.00 - 0.00 \n") + \
        std::string(nm) + std::string(" - 123.00 - 0.00 \n") + \
        std::string(nm) + std::string(" - 105.00 - 0.00 \n"); 
    EXPECT_STREQ(ans.c_str(), capturedStdout.c_str());
}
*/

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}