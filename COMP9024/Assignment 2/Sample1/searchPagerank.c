#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Define Data
#define MAX_URL_LENGTH 1005
#define MAX_WORD_LENGTH 1005

// Url Linkedlist Structure
struct UrlListNode
{
    char url[MAX_URL_LENGTH];
    struct UrlListNode * next;   // node->next
};

// Linked Nodes Structure
struct WordListNode
{
    char word[MAX_WORD_LENGTH];
    struct WordListNode * next; // node->next
    struct UrlListNode * urls;
};

// create word node head & tail
struct WordListNode * words_head = NULL;
struct WordListNode * words_tail = NULL;

// find the word
struct WordListNode * find_word(struct WordListNode * cur, char word[])
{
    if(cur == NULL)     // if empty
        return NULL;

    if(strcmp(cur->word, word) == 0)    // find the word
        return cur;

    return find_word(cur->next, word);  // check next
}

// check the url in linked list or not
int contain_url(struct UrlListNode * cur, char url[])
{
    if(cur == NULL)     // if empty
        return 0;

    if(strcmp(cur->url, url) == 0)  // find the url
        return 1;

    return contain_url(cur->next, url); // check next
}

// check word and url are in the same group
int contain(char word[], char url[])
{
    struct WordListNode * list = find_word(words_head, word);
    return contain_url(list->urls, url);
}

// url linked list
struct URLStructNode
{
    char url[MAX_URL_LENGTH];       // url
    int degree;                     // degree of each url
    double rank;                    // value of pagerank
    struct URLStructNode * next;
};

// create url node head & tail
struct URLStructNode * url_head = NULL;
struct URLStructNode * url_tail = NULL;

// readfile invertedindex.txt
void read_inverted_index()
{
    FILE * fp = fopen("invertedIndex.txt", "r");

    char line[MAX_WORD_LENGTH];
    while(fgets(line, MAX_WORD_LENGTH, fp))
    {
        if(line[strlen(line) - 1] == '\n')  // change \n to \0
            line[strlen(line) - 1] = '\0';
        if(strlen(line) == 0)               // if line is empty
            continue;

        char *ptr,*retptr;
        int i=0;

        ptr = line;
        struct WordListNode * word_node = (struct WordListNode *) malloc(sizeof(struct WordListNode));  // allocate space for word node
        struct UrlListNode * node_head = NULL;
        struct UrlListNode * node_tail = NULL;

        while ((retptr=strtok(ptr, " ")) != NULL) {
            if(i == 0)
            {
                strcpy(word_node->word, retptr);
//                printf("%s\n", word_node->word);
            }
            else
            {
                struct UrlListNode * node = (struct UrlListNode *) malloc(sizeof(struct UrlListNode));
                strcpy(node->url, retptr);
//                printf("init %s\n", node->url);
                node->next = NULL;
                if(node_tail == NULL)
                {
                    node_head = node;
                    node_tail = node;
                }
                else
                {
                    node_tail->next = node;
                    node_tail = node_tail->next;
                }
            }
            i++;
            ptr = NULL;
        }
        word_node->urls = node_head;
        if(words_tail == NULL)
        {
            words_tail = word_node;
            words_head = word_node;
        }
        else
        {
            words_tail->next = word_node;
            words_tail = words_tail->next;
        }
    }

    fclose(fp);
}

// get url rank
double get_rank(char url[])
{
    struct URLStructNode * cur = url_head;  // creaete current node for url list
    while(1)
    {
        if(cur == NULL)     // if empty
            return 0;
        if(strcmp(url, cur->url) == 0)  // find the url
            return cur->rank;           // return the rank value of url
        cur = cur->next;                // check next
    }
}

// readfile pagerankList.txt
void read_urls_datas()
{
    FILE * fp = fopen("pagerankList.txt", "r");

    char line[MAX_WORD_LENGTH];
    while(fgets(line, MAX_WORD_LENGTH, fp))
    {
        if(line[strlen(line) - 1] == '\n')
            line[strlen(line) - 1] = '\0';
        if(strlen(line) == 0)
            continue;

        char *ptr,*retptr;
        int i=0;

        ptr = line;

        struct URLStructNode * node = (struct URLStructNode *) malloc(sizeof(struct URLStructNode));
        while ((retptr=strtok(ptr, ", ")) != NULL) {
            if(i == 0)
            {
                strcpy(node->url, retptr);
            }
            else if(i == 1)
            {
                node->degree = atoi(retptr);
            }
            else if(i == 2)
            {
                node->rank = atof(retptr);
            }
            i++;
            ptr = NULL;
        }
        if(url_tail == NULL)
        {
            url_head = node;
            url_tail = node;
        }
        else
        {
            url_tail->next = node;
            url_tail = url_tail->next;
        }
    }

    fclose(fp);
}

// check and print proper result
void deal(int argc, char *argv[])
{
    struct URLStructNode * url_cur = url_head;
    while(1)
    {
        if(url_cur == NULL)     // if url list is empty
            break;
//        printf("searching %s\n", url_cur->url);

        int ok = 1;
        for(int i=1; i<argc; i++)   // read parameters
        {
            if(contain(argv[i], url_cur->url) == 0) // check each url cotains the word or not
            {
                ok = 0;
            }
        }

        if(ok == 1)     // if find the word
        {
            printf("%s\n", url_cur->url);   // print the url address
        }
        url_cur = url_cur->next;    // check next url
    }
}

int main(int argc, char *argv[]) {

    read_urls_datas();          // readfile pagerankList.txt

    read_inverted_index();      // readfile invertedIndex.txt

    deal(argc, argv);           // find word in url

    return 0;

}



