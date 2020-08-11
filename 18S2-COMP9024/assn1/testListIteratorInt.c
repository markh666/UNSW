/*
  client to test listIteratorInt.
  Written by ....
*/

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include "listIteratorInt.h"


int main(int argc, char *argv[])
{


    int val, result;


    IteratorInt it1 = IteratorIntNew();

    val = 25;
    result = add(it1, val);
    printf("Inserting %d: %s \n", val, (result==1 ? "Success" : "Failed") );
    // "Inserting 25: Success"

    val = 12;
    result = add(it1, val);
    printf("Inserting %d: %s \n", val, (result==1 ? "Success" : "Failed") );
    // "Inserting 12: Success"

    val = 6;
    result = add(it1, val);
    printf("Inserting %d: %s \n", val, (result==1 ? "Success" : "Failed") );
    // "Inserting 6: Success"

    val = 82;
    result = add(it1, val);
    printf("Inserting %d: %s \n", val, (result==1 ? "Success" : "Failed") );
    // "Inserting 82: Success"

    val = 11;
    result = add(it1, val);
    printf("Inserting %d: %s \n", val, (result==1 ? "Success" : "Failed") );
    // "Inserting 11: Success"

    result = hasNext(it1);	//hasNext的边界
    printf("Next: %s \n", (result==1 ? "Success" : "Failed") );
    // "Next: Failed"

    int *vp1 = findNext(it1, 82);	//findNext如果后边没有这个数字的情况
    if(vp1==NULL)
        printf("Next value is: NULL\n");
    else
        printf("Next value is: %d \n", *vp1 );
    // "Next value is: NULL"

    int *vp2 = previous(it1);	//输出前一个值
    printf("Previous value is: %d \n", *vp2 );
    // "Previous value is: 11"

    int *vp3 = previous(it1);
    printf("Previous value is: %d \n", *vp3 );
    // "Previous value is: 82"

    int *vp4 = previous(it1);
    printf("Previous value is: %d \n", *vp4 );
    // "Previous value is: 6"

    int *vp5 = next(it1);
    printf("Next value is: %d \n", *vp5 );
    // "Next value is: 6"

    result = deleteElm(it1);	//删除上调指令返回的值
    printf("Delete: %s \n", (result==1 ? "Success" : "Failed") );
    // "Delete: Success" and delete 6

    result = deleteElm(it1);	//因为上条指令没有返回值，所以delete失败
    printf("Delete: %s \n", (result==1 ? "Success" : "Failed") );
    // "Delete: Failed"

    int *vp6 = previous(it1);
    printf("Previous value is: %d \n", *vp6 );
    // "Previous value is: 12"

    result = set(it1, 123);	//替换上条指令返回值
    printf("Set: %s \n", (result==1 ? "Success" : "Failed") );
    // "Set: Success"

    result = set(it1, 100);	//上条指令没有返回值，所以失败
    printf("Set: %s \n", (result==1 ? "Success" : "Failed") );
    // "Set: Failed"

    int *vp61 = next(it1);
    printf("Next value is: %d \n", *vp61 );
    // "Next value is: 123"

    int *vp7 = previous(it1);
    printf("Previous value is: %d \n", *vp7 );
    // "Previous value is: 123"

    int *vp71 = previous(it1);
    printf("Previous value is: %d \n", *vp71 );
    // "Previous value is: 25"

    int *vp8 = previous(it1);	//测试到头后，是否会出现null
    if(*vp8==-1)
        printf("Previous value is: NULL \n");
    else
        printf("Previous value is: %d \n", *vp8 );
    // "Previous value is: NULL" （光标到了25前边）

    int *vp9 = next(it1);
    printf("Next value is: %d \n", *vp9 );
    // "Next value is: 25"

    result = set(it1, 105);	//替换25
    printf("Set: %s \n", (result==1 ? "Success" : "Failed") );
    // "Set: Success"

    int *vp51 = next(it1);
    printf("Next value is: %d \n", *vp51 );
    // "Next value is: 123"

    int *vp52 = next(it1);
    printf("Next value is: %d \n", *vp52 );
    // "Next value is: 82"

    reset(it1);	//重置数据

    val = 899;
    result = add(it1, val);
    printf("Inserting %d: %s \n", val, (result==1 ? "Success" : "Failed") );
    // "Inserting 899: Success"

    //reset(it1);

    int *vp91 = next(it1);
    printf("Next value is: %d \n", *vp91 );
    // "Next value is: 899"

    int *vp92 = next(it1);
    printf("Next value is: %d \n", *vp92 );
    // "Next value is: 105"

    return EXIT_SUCCESS;
}
