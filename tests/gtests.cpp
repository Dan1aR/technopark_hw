#include "gtest/gtest.h"

extern "C" {
    #include "libdtools.h"
}

// CONSTS
const char * _USERS_FILE_PATH = "../files/users/";
const char * _OBJS_FILE_PATH = "../files/objs/";
const char * _OBJS_RANK_FILE = "../files/objs_rank";

TEST(TEST_CONS, CONSIST_REC_500_USERS) {
    __generate_data__(1000, 500, 100, _USERS_FILE_PATH, _OBJS_FILE_PATH);

    int create_rec_c_exit_code = create_recomendations(_USERS_FILE_PATH, _OBJS_FILE_PATH, _OBJS_RANK_FILE, 0); 
    EXPECT_EQ(0, create_rec_c_exit_code); 

    __clean_up__(_USERS_FILE_PATH, _OBJS_FILE_PATH);
}


int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
