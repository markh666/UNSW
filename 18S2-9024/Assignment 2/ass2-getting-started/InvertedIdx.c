/*
 Inverted Index ADT (partial) implementation, written by Ashesh Mahidadia Jan 2018.
 You may need to modify the following implementation and test it properly before using 
 in your program.
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "InvertedIdx.h"
#include "DLListStr.h"

#define MAXSTRING 100      // maximum line number is 1000

#define data(tree)  ((tree)->data)
#define left(tree)  ((tree)->left)
#define right(tree) ((tree)->right)

typedef struct Node {
   Tree left, right;
   char  data[100];
   DLListStr  list;	
} Node;

// make a new node containing data
Tree newNode(Item it) {
   Tree new = malloc(sizeof(Node));
   assert(new != NULL);
   strcpy(new->data, it);  // replace,   data(new) = it;
   left(new) = right(new) = NULL;
   return new;
}

// create a new empty Tree
Tree newTree() {
   return NULL;
}

// free memory associated with Tree
void freeTree(Tree t) {
   if (t != NULL) {
      freeTree(left(t));
      freeTree(right(t));
      free(t);
   }
}

// display Tree sideways
void showTreeR(Tree t, int depth) {
   if (t != NULL) {
      showTreeR(right(t), depth+1);
      int i;
      for (i = 0; i < depth; i++)
	 putchar('\t');            // TAB character
      printf("%s\n", data(t));
      showTreeR(left(t), depth+1);
   }
}

void showTree(Tree t) {
   showTreeR(t, 0);
}

// check whether a key is in a Tree
bool TreeSearch(Tree t, Item it) {
   if (t == NULL)
      return false;

   else if (strcmp(it, data(t)) < 0)   //replace, else if (it < data(t))
      return TreeSearch(left(t), it);
   
   else if (strcmp(it, data(t)) > 0)  //replace, else if (it > data(t))
      return TreeSearch(right(t), it);

   else                                 // it == data(t)
      return true;
}

// insert a new item into a Tree
Tree TreeInsert(Tree t, Item it) {
   if (t == NULL)
      t = newNode(it);

   else if (strcmp(it, data(t)) < 0)   //replace, else if (it < data(t))
      left(t) = TreeInsert(left(t), it);

   else if (strcmp(it, data(t)) > 0)  //replace, else if (it > data(t))
      right(t) = TreeInsert(right(t), it);

   return t;
}

int main () {
   Tree t = newTree();
   printf("sss");
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
                showTree(t);
                //strcpy(content[count], token);
                //printf("%s\n", content[count]);
                //count++;
            }
            token = strtok(NULL, delim);
        } 
    }
    showTreeR(t, 1);
    return 0;
}