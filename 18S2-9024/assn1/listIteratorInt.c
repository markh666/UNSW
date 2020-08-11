/*
  listIteratorInt.c : list Iterator ADT implementation
  Date: Dec 26, 2018 updated111
*/

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include "listIteratorInt.h"

struct ListNode
{
    int     value;           // value of this list item (int)
    struct  ListNode *prev;  // pointer previous node in list
    struct  ListNode *next;  // pointer to next node in list
};

typedef struct ListNode Node;

typedef struct IteratorIntRep
{
    int nitems; // count of items in list
    Node *head; // first node in list
    Node *curr; // current node in list
    Node *tail; // last node in list
    Node *pass; // record the returned value (for next, previous, findnext, findprevious)
} IteratorIntRep;

static Node *newNode(int it)
{
    Node *new;
    new = malloc(sizeof(Node)); // reserve space for Node
    assert(new != NULL);
    new->value = it;            // it becomes node value
    new->prev = NULL;
    new->next = NULL;
    return new;
}

IteratorInt IteratorIntNew()    // create a empty Linked List
{
    struct IteratorIntRep *L;
    L = malloc(sizeof (struct IteratorIntRep));
    assert (L != NULL);
    L->nitems = 0;
    L->head = NULL;
    L->tail = NULL;
    L->curr = NULL;
    return L;
}



int add(IteratorInt it, int v)      // add a value to Linked List
{
    Node *new = newNode(v);
    assert(new != NULL);
    it->pass = NULL;
    // create a new LL if there is no
    if (it->head == NULL && it->tail == NULL)
    {
        Node *p=newNode(-1);        // set up a head point
        it->curr = it->head = it->tail = new;
        p->next=it->curr;
        it->head->prev=p;
        it->nitems++;
        return 1;
    }

    assert(it->curr != NULL);
    // add to tail
    if (it->curr == it->tail)
    {
        new->prev = it->tail;
        it->tail->next = new;
        it->curr = it->tail = new;  // new value becomes new tail
        return 1;
    }
    // add to middle
    new->prev = it->curr;
    new->next = it->curr->next;
    it->curr->next = new;
    it->nitems++;
    it->curr = new;
    return 1;
}


int hasNext(IteratorInt it)  // check has next value or not
{
    it->pass = NULL;         // because only check for this command no return value
    if (it->curr->next != NULL)
    {
        return 1;           // has next is 1
    }
    else
    {
        return 0;           // doesn't have next is 0
    }
}

int hasPrevious(IteratorInt it) // check has previous value or not
{
    it->pass = NULL;            // no return value, so pass value is NULL
    if (it->curr != NULL)
    {
        return 1;               // has previous is 1
    }
    else
    {
        return 0;               // otherwise is 0
    }
}


int *next(IteratorInt it)                   // return next value and move cursor to next position
{
    if (it->curr->next !=NULL)              // if there is a next value
    {
        int *rt = &(it->curr->next->value); // record next value
        it->curr = it->curr->next;          // move pointer to next
        it->pass = it->curr;                // use pass to record current address
        return rt;
    }
    it->pass = NULL;                        // if there is no next value, record nothing
    return NULL;
}

int *previous(IteratorInt it)           // return previous value and move cursor to previous position
{
    if (it->curr != NULL)               // if there is a previous value
    {
        int *rt = &(it->curr->value);   // record previous value
        if(it->curr->prev!=NULL)        // especially for the head of list
        {
            it->pass = it->curr;        // use pas to record current address
            it->curr = it->curr->prev;  // move pointer to previous
        }
        return rt;
    }
    it->pass = NULL;                    // if there is no previous value, record nothing
    return NULL;
}


int deleteElm(IteratorInt it)    // delete previous returned value
{
    if (it->pass == NULL)       // check is there a returned value for last command
    {
        return 0;
    }
    else
    {
        assert(it->curr != NULL);
        Node *old = it->curr;       // record current pointer address
        if (it->nitems == 0 || old == NULL)
        {
            it->pass = NULL;
            return 0;
        }
        it->curr = it->pass;        // use address of returned value
        it->curr = it->curr->prev;  // reconstruct the linked list
        it->curr->next = it->curr->next->next;
        it->curr->next->prev = it->curr;
        it->nitems--;               // decrease the number of items
        it->pass = NULL;            // no returned value
        return 1;
    }
}


int set(IteratorInt it, int v)  // replace last returned value
{
    if (it->pass != NULL)       // check is there a returned value for last command
    {
        it->pass->value=v;      // preplace last value to new value
        it->pass = NULL;
        return 1;               // set success
    }
    else
    {
        it->pass = NULL;
        return 0;               // set failed
    }
}

int *findNext(IteratorInt it, int v)    // find next value of input value
{
    if (it->curr != NULL)
    {
        Node *old = it->curr;           // record current address
        while (it->curr->next != NULL)
        {
            if (it->curr->value == v)
            {
                it->pass = it->curr; 
                return &(it->curr->next->value);    // return next value
            }
            it->curr = it->curr->next;  // move pointer to next value
        }
        it->curr = old;                 // if there is no next value, return to old value
        it->pass = NULL;
        return NULL;
    }
    else
    {
        it->pass = NULL;
        return NULL;
    }
}

int *findPrevious(IteratorInt it, int v)    // find previous value of input value
{
    if (it->curr != NULL)
    {
        Node *old = it->curr;               // record current address
        while (it->curr->next != NULL)
        {
            if (it->curr->value == v)
            {
                it->pass = it->curr->next;
                return &(it->curr->prev->value);    // return previous value
            }
            it->curr = it->curr->prev;      // move pointer to previous value
        }
        it->curr = old;                     // if there is no previous value, return to old value
        it->pass = NULL;
        return NULL;
    }
    else
    {
        it->pass = NULL;
        return NULL;
    }
}

void reset(IteratorInt it)              // reset cursor to the starting point
{
    assert(it->curr != NULL);
    it->curr = it->head;                // current position becomes the head
    it->curr->next = it->head->next;    // connect the new head and old head
    it->curr->prev = it->head->prev;
    it->curr->value = it->head->value;
    it->pass = NULL;                    // no returned value in this stage
    it->curr=it->curr->prev;            
}

void freeIt(IteratorInt it)     // free memory
{
    assert(it->curr != NULL);
    Node *curr, *prev;
    curr = it->head;            // start from head
    while (curr != NULL)        // free cycle
    {
        prev = curr;
        curr = curr->next;
        free(prev);             // free node
    }
    free(it);                   // free pointer
    it = NULL;                  // set pointer to NULL
}

