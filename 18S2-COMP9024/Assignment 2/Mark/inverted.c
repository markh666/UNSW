#include <stdio.h>
#include <string.h>
//#include <malloc.h>
#include <math.h>
#include <stdlib.h>

// 数据定义
#define MAX_URL_NUMBER 1005
#define MAX_URL_LENGTH 105
#define MAX_WORDS_LENGTH 1005

// 定义链表结构
struct LinkedListNode
{
    char url[MAX_URL_LENGTH];
    struct LinkedListNode * next;
};

// 定义二叉搜索树
struct BST
{
    // keyword
    char word[MAX_WORDS_LENGTH];
    // 左右节点
    struct BST * left;
    struct BST * right;
    // 链表
    struct LinkedListNode * head;
};

struct BST * bst = NULL;

// 在BST节点内插入url
void add_word(struct BST * cur, char url[])
{
    if(cur->head == NULL)
    {
        struct LinkedListNode * node = (struct LinkedListNode *) malloc(sizeof(struct LinkedListNode));
        node->next = NULL;
        strcpy(node->url, url);
        cur->head = node;
        return;
    }
    if(strcmp(url, cur->head->url) < 0)
    {
        struct LinkedListNode * node = (struct LinkedListNode *) malloc(sizeof(struct LinkedListNode));
        node->next = cur->head;
        strcpy(node->url, url);
        cur->head = node;
        return;
    }
    if(strcmp(url, cur->head->url) == 0)
    {
        return;
    }
    if(cur->head->next == NULL)
    {
        struct LinkedListNode * node = (struct LinkedListNode *) malloc(sizeof(struct LinkedListNode));
        node->next = NULL;
        strcpy(node->url, url);
        cur->head->next = node;
        return;
    }
    struct LinkedListNode * list = cur->head;
    while(1)
    {
        if(list->next == NULL)
        {
            struct LinkedListNode * node = (struct LinkedListNode *) malloc(sizeof(struct LinkedListNode));
            node->next = NULL;
            strcpy(node->url, url);
            list->next = node;
            return;
        }
        if(strcmp(url, list->next->url) == 0)
        {
            return;
        }
        if(strcmp(url, list->next->url) < 0)
        {
            struct LinkedListNode * node = (struct LinkedListNode *) malloc(sizeof(struct LinkedListNode));
            node->next = list->next;
            strcpy(node->url, url);
            list->next = node;
            return;
        }
        list = list->next;
    }
}

// 添加对应的word和url
void add(char word[], char url[])
{
    if(bst == NULL)
    {
        bst = (struct BST *) malloc(sizeof(struct BST));
        bst->head = NULL;
        bst->left = NULL;
        bst->right = NULL;
        strcpy(bst->word, word);
        add_word(bst, url);
        return;
    }
    struct BST * cur = bst;
    while(1)
    {
        if(strcmp(word, cur->word) == 0)
        {
            add_word(cur, url);
            return;
        }
        else if(strcmp(word, cur->word) < 0)
        {
            if(cur->left == NULL)
            {
                struct BST * node = (struct BST *) malloc(sizeof(struct BST));
                node->head = NULL;
                node->left = NULL;
                node->right = NULL;
                strcpy(node->word, word);
                add_word(node, url);
                cur->left = node;
                return;
            }
            else
            {
                cur = cur->left;
            }
        }
        else
        {
            if(cur->right == NULL)
            {
                struct BST * node = (struct BST *) malloc(sizeof(struct BST));
                node->head = NULL;
                node->left = NULL;
                node->right = NULL;
                strcpy(node->word, word);
                add_word(node, url);
                cur->right = node;
                return;
            }
            else
            {
                cur = cur->right;
            }
        }
    }
}

// 化简单词，去掉空格，标点，大小写
void simplify(char word[])
{
    char newword[MAX_WORDS_LENGTH] = {0};
    int n = 0;
    for(int i=0;i<strlen(word);i++)
    {
        if(word[i] >= 'a' && word[i] <= 'z')
        {
            newword[n++] = word[i];
        }
        else if(word[i] >= 'A' && word[i] <= 'Z')
        {
            newword[n++] = word[i] - 'A' + 'a';
        }
    }
    for(int i=0;i<MAX_WORDS_LENGTH;i++)
    {
        word[i] = newword[i];
    }
}

// 读取页面信息
void read_page(char url[])
{
    char filename[MAX_URL_LENGTH] = {0};
    strcat(filename, url);
    strcat(filename, ".txt");
    FILE * fp = fopen(filename, "r");
    char tem[MAX_WORDS_LENGTH] = {0};
    fscanf(fp, "%s", tem);
    fscanf(fp, "%s", tem);

    while(1)
    {
        fscanf(fp, "%s", tem);
        if(strcmp(tem, "#end") == 0)
            break;
    }

    fscanf(fp, "%s", tem);
    fscanf(fp, "%s", tem);
    fscanf(fp, "%s", tem);

    while(1)
    {
        fscanf(fp, "%s", tem);
        if(strcmp(tem, "#end") == 0)
            break;
        simplify(tem);
        add(tem, url);
    }

    fclose(fp);
}

// 读取collection.txt
void read_urls()
{
    FILE * fp = fopen("collection.txt", "r");
    char url[MAX_URL_LENGTH] = {0};
    while(fscanf(fp, "%s", url) != EOF)
    {
        read_page(url);
    }
    fclose(fp);
}

// 打印链表
void print_list(FILE * fp, struct LinkedListNode * list)
{
    if(list == NULL)
        return;
    fprintf(fp, " %s", list->url);
    print_list(fp, list->next);
}

// 遍历二叉树
void search(FILE * fp, struct BST * cur)
{
    if(cur == NULL)
        return;
    search(fp, cur->left);
    fprintf(fp, "%s", cur->word);
    print_list(fp, cur->head);
    fprintf(fp, "\n");
    search(fp, cur->right);
}

// 输出结果
void output()
{
    FILE * fp = fopen("invertedIndex.txt", "w");
    search(fp, bst);
    fclose(fp);
}

int main(int argc, char *argv[]) {
    setbuf(stdout, NULL);

    read_urls();

    output();

    return 0;
}

