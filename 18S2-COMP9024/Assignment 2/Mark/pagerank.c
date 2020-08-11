#include <stdio.h>
#include <string.h>
//#include <malloc.h>
#include <math.h>
#include <stdlib.h>

// 数据定义
#define MAX_URL_NUMBER 1005
#define MAX_URL_LENGTH 105
#define MAX_WORDS_LENGTH 1005

// 定义链表结构体
struct LinkedListNode
{
    char keyword[MAX_WORDS_LENGTH];
    struct LinkedListNode * next;
};

// 定义领接表
struct Matrix
{
    char url[MAX_URL_LENGTH];   // url
    int next[MAX_URL_NUMBER];   // 领接
    struct LinkedListNode * head;   // 链表头指针
    struct LinkedListNode * tail;   // 链表尾指针
    double rank_value;              // pagerank值
    int degree;                     // 度数
};

// 定义
struct Matrix urls[MAX_URL_NUMBER];
int urls_count = 0;

// 根据url找index
int find_index_by_url(char url[])
{
    for(int i=0;i<urls_count;i++)
    {
        if(strcmp(urls[i].url, url) == 0)
            return i;
    }
    return -1;
}

// 读取页面信息
void read_page(char url[], int index)
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
        int next_index = find_index_by_url(tem);
        urls[index].next[next_index] = 1;
    }

    fscanf(fp, "%s", tem);
    fscanf(fp, "%s", tem);
    fscanf(fp, "%s", tem);

    while(1)
    {
        fscanf(fp, "%s", tem);
        if(strcmp(tem, "#end") == 0)
            break;
        struct LinkedListNode * node = (struct LinkedListNode * ) malloc(sizeof(struct LinkedListNode));
        strcpy(node->keyword, tem);
        node->next = NULL;
        if(urls[index].tail == NULL)
        {
            urls[index].head = node;
            urls[index].tail = node;
        }
        else
        {
            urls[index].tail->next = node;
            urls[index].tail = urls[index].tail->next;
        }
    }

    fclose(fp);
}

// 读取collection.txt
void read_urls()
{
    FILE * fp = fopen("collection.txt", "r");

    while(fscanf(fp, "%s", urls[urls_count].url) != EOF)
    {
        urls[urls_count].head = NULL;
        urls[urls_count].tail = NULL;
        urls_count++;
    }
    fclose(fp);

    for(int i=0;i<urls_count;i++)
    {
        read_page(urls[i].url, i);
    }

}

// 计算degree
int getDegree(int index)
{
    int sum = 0;
    for(int i=0;i<urls_count;i++)
    {
        if(urls[index].next[i] > 0)
        {
            sum += 1;
        }
    }
    return sum;
}

// 计算pagerank
void PageRank(double d, double diffPR, int maxIterations)
{
    double * pr_old = (double * ) malloc(sizeof(double) * urls_count);
    double * pr = (double * ) malloc(sizeof(double) * urls_count);
    for(int i=0;i<urls_count;i++)
        pr_old[i] = (double) 1 / urls_count;
    int iteration = 0;
    double diff = diffPR;
    while(iteration < maxIterations && diff >= diffPR)
    {
        iteration++;
        for(int i=0;i<urls_count;i++)
        {
            pr[i] = 0;
            for(int j=0;j<urls_count;j++)
            {
                if(urls[j].next[i] > 0)
                {
                    pr[i] += d * pr_old[j] / getDegree(j);
                }
            }
            pr[i] += (double) (1 - d) / urls_count;
        }
        diff = 0;
        for(int i=0;i<urls_count;i++)
        {
            diff += fabs(pr[i] - pr_old[i]);
        }

        for(int i=0;i<urls_count;i++)
        {
            pr_old[i] = pr[i];
        }
    }

    for(int i=0;i<urls_count;i++)
        urls[i].rank_value = pr[i];

    free(pr);
    free(pr_old);
}

// 输出结果
void output()
{
    struct Matrix * b = (struct Matrix *) malloc(sizeof(struct Matrix) * urls_count);
    for(int i=0;i<urls_count;i++)
    {
        strcpy(b[i].url, urls[i].url);
        b[i].rank_value = urls[i].rank_value;
        b[i].degree = getDegree(i);
    }
    for(int i=0;i<urls_count;i++)
    {
        for(int j = i + 1;j<urls_count;j++)
        {
            if(b[i].rank_value < b[j].rank_value)
            {
                char tem[MAX_URL_LENGTH];
                strcpy(tem, b[i].url);
                strcpy(b[i].url, b[j].url);
                strcpy(b[j].url, tem);
                double x = b[i].rank_value;
                b[i].rank_value = b[j].rank_value;
                b[j].rank_value = x;
                int y = b[i].degree;
                b[i].degree = b[j].degree;
                b[j].degree = y;
            }
        }
    }
    FILE * fp = fopen("pagerankList.txt", "w");
    for(int i=0;i<urls_count;i++)
    {
        fprintf(fp, "%s, %d, %.7f\n", b[i].url, b[i].degree, b[i].rank_value);
    }
    fclose(fp);
    free(b);
}

int main(int argc, char *argv[]) {
    setbuf(stdout, NULL);

    double d = atof(argv[1]);
    double diffPR = atof(argv[2]);
    int maxIterations = atoi(argv[3]);

    memset(urls, 0, sizeof(urls));
    urls_count = 0;

    read_urls();

    PageRank(d, diffPR, maxIterations);

    output();

    return 0;
}

