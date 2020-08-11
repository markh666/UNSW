#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "InvertedIdx.h"

#define MAXSTRING 100      // maximum line number is 1000

int main () {
   Tree t = newTree();
   char delim[2] = " ";
   char *token, p, temp[5], line[MAXSTRING];
   char mid[] = {"Section-2"}, start[] = {"#start"}, end[] = {"#end"};
   int array[MAXSTRING], count = 0, j, T = 0;
   char content[MAXSTRING][100];
   FILE *f;

    if ((f = fopen ("url31.txt", "r")) == NULL) {  // if the file is empty, output an error
        printf("Error!\n");
        return 0;
    }
    while(fgets(line, MAXSTRING, f) != NULL)  {     // if the file is not empty, read lines
        
        token = strtok(line, delim);        // the first string of a line

        while (token != NULL && T == 0) {
            if (token[0] == 'S' && token[7] == '-' && token[8] == '2') {
                T = 1;
            }
            token = strtok(NULL, delim);
        }

        while (token != NULL && T == 1) {
            if (strcmp(token, end) == 0)
                break;
            else
            {
                int l;
                for (l = 0; token[l] != '\0'; l++) {
                    if (token[l] < 'A' || token[l] > 'z' || (token[l] > 'Z' && token[l] < 'a'))
                        token[l] = '\0';

                    else if (token[l] >= 'A' && token[l] <= 'Z') 
                        token[l] += 32;
                }
                if (token[0] < 'A' || token[0] > 'z') {
                    break;
                }
                TreeInsert(t, token);
                //strcpy(content[count], token);
                //printf("%s\n", content[count]);
                count++;
            }
            token = strtok(NULL, delim);
        } 
    }
    /*for (int z = 0; z < count; z++) {
        printf("word is : %s\n", content[z]);
    }*/
    showTree(t);
    return 0;
}