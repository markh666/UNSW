// reln.c ... functions on Relations
// part of Multi-attribute Linear-hashed Files
// Last modified by John Shepherd, July 2019

#include "defs.h"
#include "reln.h"
#include "page.h"
#include "tuple.h"
#include "chvec.h"
#include "bits.h"
#include "hash.h"

#define HEADERSIZE (3*sizeof(Count)+sizeof(Offset))

struct RelnRep {
	Count  nattrs; // number of attributes
	Count  depth;  // depth of main data file
	Offset sp;     // split pointer
    Count  npages; // number of main data pages
    Count  ntups;  // total number of tuples
	ChVec  cv;     // choice vector
	char   mode;   // open for read/write
	FILE  *info;   // handle on info file
	FILE  *data;   // handle on data file
	FILE  *ovflow; // handle on ovflow file
};

// create a new relation (three files)

Status newRelation(char *name, Count nattrs, Count npages, Count d, char *cv)
{
    char fname[MAXFILENAME];
	Reln r = malloc(sizeof(struct RelnRep));
	r->nattrs = nattrs; r->depth = d; r->sp = 0;
	r->npages = npages; r->ntups = 0; r->mode = 'w';
	assert(r != NULL);
	if (parseChVec(r, cv, r->cv) != OK) return ~OK;
	sprintf(fname,"%s.info",name);
	r->info = fopen(fname,"w");
	assert(r->info != NULL);
	sprintf(fname,"%s.data",name);
	r->data = fopen(fname,"w");
	assert(r->data != NULL);
	sprintf(fname,"%s.ovflow",name);
	r->ovflow = fopen(fname,"w");
	assert(r->ovflow != NULL);
	int i;
	for (i = 0; i < npages; i++) addPage(r->data);
	closeRelation(r);
	return 0;
}

// check whether a relation already exists

Bool existsRelation(char *name)
{
	char fname[MAXFILENAME];
	sprintf(fname,"%s.info",name);
	FILE *f = fopen(fname,"r");
	if (f == NULL)
		return FALSE;
	else {
		fclose(f);
		return TRUE;
	}
}

// set up a relation descriptor from relation name
// open files, reads information from rel.info

Reln openRelation(char *name, char *mode)
{
	Reln r;
	r = malloc(sizeof(struct RelnRep));
	assert(r != NULL);
	char fname[MAXFILENAME];
	sprintf(fname,"%s.info",name);
	r->info = fopen(fname,mode);
	assert(r->info != NULL);
	sprintf(fname,"%s.data",name);
	r->data = fopen(fname,mode);
	assert(r->data != NULL);
	sprintf(fname,"%s.ovflow",name);
	r->ovflow = fopen(fname,mode);
	assert(r->ovflow != NULL);
	// Naughty: assumes Count and Offset are the same size
	int n = fread(r, sizeof(Count), 5, r->info);
	assert(n == 5);
	n = fread(r->cv, sizeof(ChVecItem), MAXCHVEC, r->info);
	assert(n == MAXCHVEC);
	r->mode = (mode[0] == 'w' || mode[1] =='+') ? 'w' : 'r';
	return r;
}

// release files and descriptor for an open relation
// copy latest information to .info file

void closeRelation(Reln r)
{
	// make sure updated global data is put in info
	// Naughty: assumes Count and Offset are the same size
	if (r->mode == 'w') {
		fseek(r->info, 0, SEEK_SET);
		// write out core relation info (#attr,#pages,d,sp)
		int n = fwrite(r, sizeof(Count), 5, r->info);
		assert(n == 5);
		// write out choice vector
		n = fwrite(r->cv, sizeof(ChVecItem), MAXCHVEC, r->info);
		assert(n == MAXCHVEC);
	}
	fclose(r->info);
	fclose(r->data);
	fclose(r->ovflow);
	free(r);
}

// insert a new tuple into a relation
// returns index of bucket where inserted
// - index always refers to a primary data page
// - the actual insertion page may be either a data page or an overflow page
// returns NO_PAGE if insert fails completely
// TODO: include splitting and file expansion

PageID addToRelation(Reln r, Tuple t)
{
	int nt = r->ntups + 1, na = r->nattrs;
	int zero_con = (nt % (1024 / (10 * na)) == 0);
	if (zero_con)
	{
		//Start spliting
		splitReln(r);
	}
	
	Bits h, p;
	// char buf[MAXBITS+1];
	h = tupleHash(r,t);
	if (r->depth == 0)
		p = 1;
	else {
		p = getLower(h, r->depth);
		if (p < r->sp) p = getLower(h, r->depth+1);
	}
	// bitsString(h,buf); printf("hash = %s\n",buf);
	// bitsString(p,buf); printf("page = %s\n",buf);
	Page pg = getPage(r->data,p);
	if (addToPage(pg,t) == OK) {
		putPage(r->data,p,pg);
		r->ntups++;
		return p;
	}
	// primary data page full
	if (pageOvflow(pg) == NO_PAGE) {
		// add first overflow page in chain
		PageID newp = addPage(r->ovflow);
		pageSetOvflow(pg,newp);
		putPage(r->data,p,pg);
		Page newpg = getPage(r->ovflow,newp);
		// can't add to a new page; we have a problem
		if (addToPage(newpg,t) != OK) return NO_PAGE;
		putPage(r->ovflow,newp,newpg);
		r->ntups++;
		return p;
	}
	else {
		// scan overflow chain until we find space
		// worst case: add new ovflow page at end of chain
		Page ovpg, prevpg = NULL;
		PageID ovp, prevp = NO_PAGE;
		ovp = pageOvflow(pg);
		while (ovp != NO_PAGE) {
			ovpg = getPage(r->ovflow, ovp);
			if (addToPage(ovpg,t) != OK) {
				prevp = ovp; prevpg = ovpg;
				ovp = pageOvflow(ovpg);
			}
			else {
				if (prevpg != NULL) free(prevpg);
				putPage(r->ovflow,ovp,ovpg);
				r->ntups++;
				return p;
			}
		}
		// all overflow pages are full; add another to chain
		// at this point, there *must* be a prevpg
		assert(prevpg != NULL);
		// make new ovflow page
		PageID newp = addPage(r->ovflow);
		// insert tuple into new page
		Page newpg = getPage(r->ovflow,newp);
        if (addToPage(newpg,t) != OK) return NO_PAGE;
        putPage(r->ovflow,newp,newpg);
		// link to existing overflow chain
		pageSetOvflow(prevpg,newp);
		putPage(r->ovflow,prevp,prevpg);
        r->ntups++;
		return p;
	}
	return NO_PAGE;
}


Status insertPage(Reln r, Tuple t, PageID pid)
{
	Page pg = getPage(r->data,pid);

	int ok_con = (addToPage(pg, t) == OK);
	if (ok_con)
	{
		putPage(r->data, pid, pg);
		return pid;
	}
	// primary data page full
	int ov_np = (pageOvflow(pg) == NO_PAGE);
	if (ov_np)
	{
		// add first overflow page in chain
		PageID newp = addPage(r->ovflow);
		pageSetOvflow(pg, newp);
		putPage(r->data, pid, pg);
		Page newpg = getPage(r->ovflow, newp);
		// can't add to a new page; we have a problem
		int no_ok = (addToPage(newpg, t) == OK);
		if (!no_ok)
			return NO_PAGE;
		putPage(r->ovflow, newp, newpg);
		return pid;
	} 
	else
	{
		// scan overflow chain until we find space
		// worst case: add new ovflow page at end of chain
		Page ovpg, prevpg = NULL;
		PageID ovp, prevp = NO_PAGE;
		ovp = pageOvflow(pg);
		int ov_np = (ovp != NO_PAGE);
		while (ov_np)
		{
			ovpg = getPage(r->ovflow, ovp);
			int ad_ok = (addToPage(ovpg, t) != OK);
			if (!ad_ok)
			{
				int prgv = (prevpg != NULL);
				if (prgv)
					free(prevpg);
				putPage(r->ovflow, ovp, ovpg);
				return pid;
			} else
			{
				prevp = ovp;
				prevpg = ovpg;
				ovp = pageOvflow(ovpg);
			}
		}
		// all overflow pages are full; add another to chain
		// at this point, there *must* be a prevpg
		int prgv_null = (prevpg != NULL);
		assert(prgv_null);
		// make new ovflow page
		PageID newp = addPage(r->ovflow);
		// insert tuple into new page
		Page newpg = getPage(r->ovflow, newp);
		int ad_ok = (addToPage(newpg, t) == OK);
		if (!ad_ok)
			return NO_PAGE;
		putPage(r->ovflow, newp, newpg);
		// link to existing overflow chain
		pageSetOvflow(prevpg, newp);
		putPage(r->ovflow, prevp, prevpg);
		return pid;
	}
}

void splitReln(Reln r)
{
	addPage(r->data);
	r->npages++;
	//PageID addid = pid | setBit(0,r->depth);

	//Dummy approach to store all the tups stay in original page
	Tuple *tups_stay = malloc(1024 * sizeof(Tuple));

	PageID pid = r->sp;
	FILE * file = r->data;
	int index = 0;
	Offset curtup = 0;
	Count ntups = 0;

	while (pid != NO_PAGE)
	{
		Page pg = getPage(file, pid);

		int pg_tp = (pageNTuples(pg) == 0);
		if(pg_tp){
			break;
		}
		Tuple tmp = nextTuple(file, pid, curtup);
		Bits hash, newid;

		// newid is always a data page id
		hash = tupleHash(r, tmp);
		newid = getLower(hash, r->depth + 1);

		//if tuple should stay in original page
		int new_pid = (newid == pid);
		if (!new_pid)
		{
			//insert tuple in new page
			int ins_np = (insertPage(r, tmp, newid) == NO_PAGE);
			if (ins_np)
				printf("Alarm!!!!!  Insert [%s] to NEW page %d go wrong\n", tmp, newid);
		} 
		else
		{
			tups_stay[index++] = strdup(tmp);
		}
		curtup += strlen(tmp)+1;
		ntups++;

		// cur page has no more tuples
		int nt_pn = (ntups >= pageNTuples(pg));
		if (nt_pn)
		{
			//use a new empty page to cover the old one
			Page cover = newPage();
			putPage(file, pid, cover);

			pid = pageOvflow(pg);
			ntups = 0;
			curtup = 0;
			file = r->ovflow;
		}
		free(tmp);
	}

	int i;
	int upper = index;
	for (i = 0; i < upper; ++i)
	{
		Tuple tmp = tups_stay[i];
		int into_pn = (insertPage(r, tmp, r->sp) == NO_PAGE);
		if (into_pn)
			printf("Alarm!!!!!  Inserting [%s] to page %d go wrong\n", tmp, r->sp);
		free(tmp);
	}
	free(tups_stay);
	int get_low = (getLower(r->sp + 1, r->depth) == 0);
	if (get_low)
	{
		r->depth++;
		r->sp = 0;
	} else
	{
		r->sp++;
	}
}

// external interfaces for Reln data

FILE *dataFile(Reln r) { return r->data; }
FILE *ovflowFile(Reln r) { return r->ovflow; }
FILE *finfo(Reln r){return r->info;}
Count nattrs(Reln r) { return r->nattrs; }
Count npages(Reln r) { return r->npages; }
Count ntuples(Reln r) { return r->ntups; }
Count depth(Reln r)  { return r->depth; }
Count splitp(Reln r) { return r->sp; }
ChVecItem *chvec(Reln r)  { return r->cv; }


// displays info about open Reln

void relationStats(Reln r)
{
	printf("Global Info:\n");
	printf("#attrs:%d  #pages:%d  #tuples:%d  d:%d  sp:%d\n",
	       r->nattrs, r->npages, r->ntups, r->depth, r->sp);
	printf("Choice vector\n");
	printChVec(r->cv);
	printf("Bucket Info:\n");
	printf("%-4s %s\n","#","Info on pages in bucket");
	printf("%-4s %s\n","","(pageID,#tuples,freebytes,ovflow)");
	for (Offset pid = 0; pid < r->npages; pid++) {
		printf("[%2d]  ",pid);
		Page p = getPage(r->data, pid);
		Count ntups = pageNTuples(p);
		Count space = pageFreeSpace(p);
		Offset ovid = pageOvflow(p);
		printf("(d%d,%d,%d,%d)",pid,ntups,space,ovid);
		free(p);
		while (ovid != NO_PAGE) {
			Offset curid = ovid;
			p = getPage(r->ovflow, ovid);
			ntups = pageNTuples(p);
			space = pageFreeSpace(p);
			ovid = pageOvflow(p);
			printf(" -> (ov%d,%d,%d,%d)",curid,ntups,space,ovid);
			free(p);
		}
		putchar('\n');
	}
}
