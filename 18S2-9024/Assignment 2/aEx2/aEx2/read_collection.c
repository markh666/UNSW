#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#define MAXSTRING 1000      // maximum line number is 1000


int main () {

   char delim[2] = " ";
   char *token, p, temp[5], line[MAXSTRING];
   int url[MAXSTRING], count = 0, j;
   FILE *f;

    if ((f = fopen ("collection.txt", "r")) == NULL) {  // if the file is empty, output an error
        printf("Error!\n");
        return 0;
    }

    while(fgets(line, MAXSTRING, f) != NULL)  {     // if the file is not empty, read lines

        token = strtok(line, delim);        // the first string of a line
        if (token[0] == '#' && token[1] == 'e' && token[2] == 'n' && token[3] == 'd') {
            break;
        }
        while( token != NULL ) {
            int r = 3;
            int i = 0;
            if (token[0] == 'u' && token[1] == 'r' && token[2] == 'l') {    // check the first three letters are 'url'

                while (token[r] != '\0') {  // start to record the url number
                    p = token[r];           // record from the fourth letter
                    temp[i] = p;
                    r++;
                    i++;
                }

                url[count] = atoi(temp);      // count the total url number
                count++;
            }
            token = strtok(NULL, delim);    // next string
        }
    }
    printf("Total url count is : %d\n", count);
    for (j = 0; j < count; j++)             // print out the url array
        printf("The link is url%d\n", url[j]);
    return 0;
    }


