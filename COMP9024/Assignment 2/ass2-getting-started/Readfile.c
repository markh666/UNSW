#include <string.h>
#include <stdio.h>

#define MAXSTRING 1000

int main() {
    char delim[2] = " ";    // one is for space another is for 0
    char *token;
    char a[MAXSTRING];      // maximum url is 1000
    char s[7] = "#start";
    char t[10] = "Section-1";
    int i = 0;
    char test[i][10];
    char line[MAXSTRING];
    FILE *f;

    if ((f = fopen ("sample1.txt", "r")) == NULL) {
        printf("Error!\n");
        return(0);
    }

        token = strtok(line, delim);
        if (token == s) {
            token = strtok(NULL, delim);
            if (token == t) {
                while(fgets(line, MAXSTRING, f) != NULL) {
                    if (token == s)
            }
        }
        while (token != NULL) {
        }   
        }        
}