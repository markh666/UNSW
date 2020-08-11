#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

// Define Data
#define MAX_URL_NUMBER 1005
#define MAX_URL_LENGTH 105
#define MAX_WORDS_LENGTH 1005

// Linked Nodes Structure
struct LinkedListNode
{
    char url[MAX_URL_LENGTH];
    struct LinkedListNode * next;   // node->next
};

// Binary Search Tree Structure
struct BST
{
    // keyword
    char word[MAX_WORDS_LENGTH];
    // left and right
    struct BST * left;
    struct BST * right;
    // Linked List
    struct LinkedListNode * head;
};

// create a new Tree bst
struct BST * bst = NULL;

// record url address to LinkedList
void add_url(struct BST * cur, char url[])
{
    if(cur->head == NULL)       // if empty
    {
        struct LinkedListNode * node = (struct LinkedListNode *) malloc(sizeof(struct LinkedListNode)); // create new node
        node->next = NULL;
        strcpy(node->url, url); // record url to linked list
        cur->head = node;       // new node becomes the head of list
        return;
    }

    if(strcmp(url, cur->head->url) < 0) // if new url less than last one
    {
        struct LinkedListNode * node = (struct LinkedListNode *) malloc(sizeof(struct LinkedListNode)); // create new node
        node->next = cur->head;     // new node becomes new head
        strcpy(node->url, url);     // copy value to node
        cur->head = node;
        return;
    }

    if(strcmp(url, cur->head->url) == 0)    // if this url address is already in list, skip
    {
        return;                             // do nothing
    }

    if(cur->head->next == NULL)     // if there is only one node && new node > last one
    {
        struct LinkedListNode * node = (struct LinkedListNode *) malloc(sizeof(struct LinkedListNode)); // create new node
        node->next = NULL;
        strcpy(node->url, url);
        cur->head->next = node;    // put new node after last
        return;
    }

    struct LinkedListNode * list = cur->head;   // create new list

    while(1)        // if there are more than one node, and new url greater than the head
    {
        if(list->next == NULL)      // Traversing to the last node
        {
            struct LinkedListNode * node = (struct LinkedListNode *) malloc(sizeof(struct LinkedListNode)); // create new node
            node->next = NULL;
            strcpy(node->url, url);
            list->next = node;      // add new node to the tail
            return;
        }

        if(strcmp(url, list->next->url) == 0)   // if find any node equal to url, break
        {
            return;                             // do nothing
        }

        if(strcmp(url, list->next->url) < 0)    // if url less than any node
        {
            struct LinkedListNode * node = (struct LinkedListNode *) malloc(sizeof(struct LinkedListNode)); // create new node
            node->next = list->next;
            strcpy(node->url, url);
            list->next = node;      // put new node before last node
            return;
        }
        list = list->next;         // move current pointer to next node
    }
}

// add word and url to BST
void add(char word[], char url[])
{
    if(bst == NULL)     // if bst is empty
    {
        bst = (struct BST *) malloc(sizeof(struct BST));    // allocate space for bst 
        bst->head = NULL;
        bst->left = NULL;
        bst->right = NULL;
        strcpy(bst->word, word);        // record the word
        add_url(bst, url);              // add url address to the linked list
        return;
    }

    struct BST * cur = bst;             // current t

    while(1)        // if bst not empty, need to compare with cur and then put word in correct position
    {
        if(strcmp(word, cur->word) == 0)    // if this word already in bst
        {
            add_url(cur, url);              // only record the url address into linked list
            return;
        }
        else if(strcmp(word, cur->word) < 0)    // if this word not in bst and less than current word
        {
            if(cur->left == NULL)               // if left is empty
            {
                struct BST * node = (struct BST *) malloc(sizeof(struct BST));  // create new node
                node->head = NULL;
                node->left = NULL;
                node->right = NULL;
                strcpy(node->word, word);
                add_url(node, url);              // record url address
                cur->left = node;                // add word to left of current
                return;
            }
            else
            {
                cur = cur->left;                // if left is not empty, check next left recursively
            }
        }
        else    // if this word not in bst and greater than current word
        {
            if(cur->right == NULL)           // if right is empty
            {
                struct BST * node = (struct BST *) malloc(sizeof(struct BST));  // create new ndoe
                node->head = NULL;
                node->left = NULL;
                node->right = NULL;
                strcpy(node->word, word);
                add_url(node, url);             // record url address
                cur->right = node;              // add word to right of current
                return;
            }
            else
            {
                cur = cur->right;           // if right is not empty, check next right recursively
            }
        }
    }
}

// Normalization words
void simplify(char word[])
{
    char newword[MAX_WORDS_LENGTH] = {0};
    int n = 0;
    for(int i=0; i<strlen(word); i++)           // if punctuation or other symbols, skip to record
    {
        if(word[i] >= 'a' && word[i] <= 'z')    // if lower letter, just record
        {
            newword[n++] = word[i];
        }
        else if(word[i] >= 'A' && word[i] <= 'Z')   // if upper letter
        {
            newword[n++] = word[i] - 'A' + 'a';     // change it to lower letter
        }
    }

    for(int i=0; i<MAX_WORDS_LENGTH; i++)       // update word after check upper letter and symbols
    {
        word[i] = newword[i];
    }
}

// readfile
void read_page(char url[])
{
    char filename[MAX_URL_LENGTH] = {0};
    strcat(filename, url);                  // add url# to filename
    strcat(filename, ".txt");               // add suffix .txt to filename
    FILE * fp = fopen(filename, "r");
    char temp[MAX_WORDS_LENGTH] = {0};
    fscanf(fp, "%s", temp);                 // use temp to record each address
    fscanf(fp, "%s", temp);                 // skip #start & Section-1

    while(1)    // read section-1
    {
        fscanf(fp, "%s", temp);       
        if(strcmp(temp, "#end") == 0)    // skip section-1
            break;
    }

    fscanf(fp, "%s", temp);  // skip "Section-1"
    fscanf(fp, "%s", temp);  // skip "#start"
    fscanf(fp, "%s", temp);  // skip "Section-2"

    while(1)    // read section-2
    {
        fscanf(fp, "%s", temp);
        if(strcmp(temp, "#end") == 0)   // has record all words, break
            break;
        simplify(temp);                 // normalization words
        add(temp, url);                 // add url to linked list
    }

    fclose(fp);
}

// readfile collection.txt
void read_urls()
{
    FILE * fp = fopen("collection.txt", "r");
    char url[MAX_URL_LENGTH] = {0};
    while(fscanf(fp, "%s", url) != EOF) // read entire page
    {
        read_page(url);                 // read each url#.txt file
    }
    fclose(fp);
}

// print out the linked list
void print_list(FILE * fp, struct LinkedListNode * list)
{
    if(list == NULL)        // if list is empty
        return;
    fprintf(fp, " %s", list->url);  // print out url address
    print_list(fp, list->next);     // print each url recursively
}

// search and print the word of bst
void search(FILE * fp, struct BST * cur)
{
    if(cur == NULL)     // if bst is empty
        return;
    search(fp, cur->left);
    fprintf(fp, "%s", cur->word);   // print out left first
    print_list(fp, cur->head);      // print url address after each word
    fprintf(fp, "\n");
    search(fp, cur->right);         // print out right side
}

// write result to invertedIndex.txt
void output()
{
    FILE * fp = fopen("invertedIndex.txt", "w");
    search(fp, bst);                // show bst
    fclose(fp);
}

int main(int argc, char *argv[]) {

    read_urls();        // read collection.txt and read each url#.txt to record data

    output();           // write result to invertedIndex.txt

    return 0;
}

