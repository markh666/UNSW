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
    struct LinkedListNode * next;   // node->next
};

// Matrix Graph to record the connection of each pair of url
struct Matrix
{
    char url[MAX_URL_LENGTH];   // url
    int next[MAX_URL_NUMBER];   
    struct LinkedListNode * head;   // node->head
    struct LinkedListNode * tail;   // node->tail
    double rank_value;              // value of pagerank
    int degree;                     // degree of each url
};

// Matrix url and url counter
struct Matrix urls[MAX_URL_NUMBER];
int urls_count = 0;

// dictionary for url
int find_index_by_url(char url[])
{
    for(int i=0; i<urls_count; i++)
    {
        if(strcmp(urls[i].url, url) == 0)   // find url index of array
            return i;
    }
    return -1;
}

// readfile
void read_page(char url[], int index)
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
        if(strcmp(temp, "#end") == 0)       // has record all url, break
            break;
        int next_index = find_index_by_url(temp);   // record array index of url
        urls[index].next[next_index] = 1;   // record connection
    }

    fclose(fp);
}

// readfile collection.txt
void read_urls()
{
    FILE * fp = fopen("collection.txt", "r");

    while(fscanf(fp, "%s", urls[urls_count].url) != EOF)    // record all url to url list
    {
        urls[urls_count].head = NULL;   // just an array, no connection with others
        urls[urls_count].tail = NULL;
        urls_count++;                   // url array index
    }
    fclose(fp);

    for(int i=0; i<urls_count; i++)
    {
        read_page(urls[i].url, i);  // read each url#.txt file
    }

}

// record degree of each url
int getDegree(int index)
{
    int sum = 0;
    for(int i=0; i<urls_count; i++)
    {
        if(urls[index].next[i] > 0)
        {
            sum += 1;   // use urls list to check how many connected urls
        }
    }
    return sum;
}

// calculate the pagerank
void PageRank(double d, double diffPR, int maxIterations)
{
    double * pr_old = (double * ) malloc(sizeof(double) * urls_count); // create an old pr value array
    double * pr = (double * ) malloc(sizeof(double) * urls_count);  // create a current pr value array
    for(int i=0; i<urls_count; i++)
        pr_old[i] = (double) 1 / urls_count;    // 1/N, initial value
    int iteration = 0;
    double diff = diffPR;
    while(iteration < maxIterations && diff >= diffPR)  // iteration times less than max &&
    {                                                   // differences greater than diffPR value
        iteration++;
        for(int i=0; i<urls_count; i++)
        {
            pr[i] = 0;
            for(int j=0; j<urls_count; j++)
            {
                if(urls[j].next[i] > 0)
                {
                    pr[i] += d * pr_old[j] / getDegree(j);  // sum (d * PR / L)
                }
            }
            pr[i] += (double) (1 - d) / urls_count;     // (1 - d) / N
        }
        diff = 0;   // calculate the diff value between new and old
        for(int i=0;i<urls_count;i++)
        {
            diff += fabs(pr[i] - pr_old[i]);    // the absolute value of diff
        }

        for(int i=0;i<urls_count;i++)   // update pr value
        {
            pr_old[i] = pr[i];  // current value becomes old value
        }
    }

    for(int i=0; i<urls_count; i++)     // record each pr value to urls list
        urls[i].rank_value = pr[i];

    free(pr);
    free(pr_old);
}

// output the result
void output()
{
    struct Matrix * b = (struct Matrix *) malloc(sizeof(struct Matrix) * urls_count);   // create a new list for record values in order
    for(int i=0; i<urls_count; i++)     // copy url list to b
    {
        strcpy(b[i].url, urls[i].url);          // copy url
        b[i].rank_value = urls[i].rank_value;   // copy pagerank value
        b[i].degree = getDegree(i);             // copy degree
    }
    for(int i=0;i<urls_count;i++)
    {
        for(int j = i + 1; j<urls_count; j++)
        {
            if(b[i].rank_value < b[j].rank_value)   // if rank value of b[i] < b[i+1]
            {
                char temp[MAX_URL_LENGTH];
                strcpy(temp, b[i].url);             // use temp to record data of b[i]
                strcpy(b[i].url, b[j].url);
                strcpy(b[j].url, temp);             // swap value
                double x = b[i].rank_value;
                b[i].rank_value = b[j].rank_value;  
                b[j].rank_value = x;                
                int y = b[i].degree;
                b[i].degree = b[j].degree;
                b[j].degree = y;
            }
        }
    }
    FILE * fp = fopen("pagerankList.txt", "w"); // write result to pagerankList.txt file
    for(int i=0; i<urls_count; i++)
    {
        fprintf(fp, "%s, %d, %.7lf\n", b[i].url, b[i].degree, b[i].rank_value); // output result
    }
    fclose(fp);
    free(b);
}

int main(int argc, char *argv[]) {

    double d = atof(argv[1]);           // read input value of d
    double diffPR = atof(argv[2]);      // read input value of diffPR
    int maxIterations = atoi(argv[3]);  // read input value of maxIterations

    urls_count = 0;

    read_urls();                        // start from read collection.txt and then read each url#.txt

    PageRank(d, diffPR, maxIterations); // caculate PR value of each url

    output();                           // output the result to "pagerankList.txt"

    return 0;
}

