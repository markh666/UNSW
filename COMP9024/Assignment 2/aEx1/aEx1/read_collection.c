#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#define MAXSTRING 1000      // maximum line number is 1000


void CreateRelation(int url[], int count) { // read each url file and record the relationships
    int **Matrix;                           // create a Matrix
    int i, j, n, l;
    char filename[25] = {"url"};
    char suffix[5] = {".txt"};
    char temp[5];                           // to store url integer
    for (i = 0; i < count; i++) {           // read each url file
        n = url[i];
        sprintf(temp, "%d", n);
        strcat(filename, temp);
        strcat(filename, suffix);
        readfile(filename);                 // read file
        for (j = 0; j < degree; j++) {      // use url[] as dic to record each url index
            for (l = 0; l < count; l++) {
                if (array[j] == url[l]) {
                    Matrix[i][l] = d * (1 / degree) + (1 - d) * 1 / count;       // find each pair url and mark it as 1
                }
                else {
                    Matrix[i][l] = (1 - d) * 1 / count;
                }
            }
        }
    }
}

void insertionSort(int array[], int n) {        // sort an array
    int i;
    for (i = 1; i < n; i++) {
        int element = array[i];                 // record the next one
        int j = i - 1;                          // point to the current
        while (j >= 0 && array[j] > element) {  // compare current & next
            array[j+1] = array[j];
            j--;
        }
        array[j+1] = element;
    }
}

int readfile (char filename) {
   char delim[2] = " ";
   char *token, p, temp[5], line[MAXSTRING];
   int url[MAXSTRING], count = 0, j;
   FILE *f;

    if ((f = fopen (filename, "r")) == NULL) {  // if the file is empty, output an error
        printf("Error!\n");
        return 0;
    }

    while(fgets(line, MAXSTRING, f) != NULL)  {     // if the file is not empty, read lines

        token = strtok(line, delim);        // the first string of a line
        if (token[0] == '#' && token[1] == 'e' && token[2] == 'n' && token[3] == 'd') {
            break;
        }
        while (token != NULL ) {
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
    //printf("Total url count is : %d\n", count);
    insertionSort(url, count);              // sort the array
    for (j = 0; j < count; j++)             // print out the url array
        printf("The link is url%d\n", url[j]);
    return 0;
    }

