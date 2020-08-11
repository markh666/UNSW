// tuple.c ... functions on tuples
// part of Multi-attribute Linear-hashed Files
// Last modified by John Shepherd, July 2019

#include "defs.h"
#include "tuple.h"
#include "reln.h"
#include "hash.h"
#include "chvec.h"
#include "bits.h"

// return number of bytes/chars in a tuple

int tupLength(Tuple t)
{
	return strlen(t);
}

// reads/parses next tuple in input

Tuple readTuple(Reln r, FILE *in)
{
	char line[MAXTUPLEN];
	if (fgets(line, MAXTUPLEN-1, in) == NULL)
		return NULL;
	line[strlen(line)-1] = '\0';
	// count fields
	// cheap'n'nasty parsing
	char *c; int nf = 1;
	for (c = line; *c != '\0'; c++)
		if (*c == ',') nf++;
	// invalid tuple
	if (nf != nattrs(r)) return NULL;
	return copyString(line); // needs to be free'd sometime
}

Tuple nextTuple(FILE *in,PageID pid,Offset cur_tup)
{
	char line[MAXTUPLEN];
	Offset base = PAGESIZE * pid + 2 * sizeof(Offset) + sizeof(Count);
	fseek(in, base + cur_tup, SEEK_SET);
	fgets(line, MAXTUPLEN - 1, in);
	return copyString(line); 
}
// extract values into an array of strings

void tupleVals(Tuple t, char **vals)
{
	char *c = t, *c0 = t;
	int i = 0;
	for (;;) {
		while (*c != ',' && *c != '\0') c++;
		if (*c == '\0') {
			// end of tuple; add last field to vals
			vals[i++] = copyString(c0);
			break;
		}
		else {
			// end of next field; add to vals
			*c = '\0';
			vals[i++] = copyString(c0);
			*c = ',';
			c++; c0 = c;
		}
	}
}

// release memory used for separate attirubte values

void freeVals(char **vals, int nattrs)
{
	int i;
	for (i = 0; i < nattrs; i++) free(vals[i]);
}

// hash a tuple using the choice vector
// TODO: actually use the choice vector to make the hash

Bits tupleHash(Reln r, Tuple t)
{
	char buf[MAXBITS + 1];
	char buf_1[MAXBITS +1];
	char tup[MAXTUPLEN];
	Count nvals = nattrs(r);
	char **vals = malloc(nvals * sizeof(char *));
	assert(vals != NULL);
	tupleVals(t, vals);
	int i,j,k;
    tupleString(t,tup);
	Bits hash[nvals];
	//Compute  hash for attrs, save them to hash[].
	int upper = nvals;
	for (i = 0; i < upper; i++)
	{
		hash[i] = hash_any((unsigned char *) vals[i], strlen(vals[i]));
		bitsString(hash[i], buf);

	}

	//According to  choice vector(c_v), insert bits to  the buffer from attr hash.
	ChVecItem *c_v = chvec(r);
	Byte attr = c_v[0].att;
	Byte bit = c_v[0].bit;
	for (i = 0; i < 32; i++)
	{
		attr = c_v[i].att;
		bit = c_v[i].bit;
		bitsString(hash[attr], buf);
		j = 0;
		k = 0;
		while (buf[j] != '\0')
		{
			int not_space=(buf[j] != ' ');
			if (not_space==1)
			{
				buf[k++] = buf[j];
			}
			j++;
		}
		buf_1[31 - i] = buf[31 - bit];
	}

	Bits result = 0xFFFFFFFF;
	for (i = 0; i < 32; i++)
	{
		int if_zero=(buf_1[i] == '0');
		if (if_zero==1)
			result = unsetBit(result, 31 - i);//Transfer buffer array into Bits.

	}
	free(vals);
	bitsString(result,buf);
	printf("hash(%s) = %s\n",tup,buf);
	return result;
}

// compare two tuples (allowing for "unknown" values)

Bool tupleMatch(Reln r, Tuple t1, Tuple t2)
{
	Count na = nattrs(r);
	char **v1 = malloc(na*sizeof(char *));
	tupleVals(t1, v1);
	char **v2 = malloc(na*sizeof(char *));
	tupleVals(t2, v2);
	Bool match = TRUE;
	int i;
	for (i = 0; i < na; i++) {
		// assumes no real attribute values start with '?'
		if (v1[i][0] == '?' || v2[i][0] == '?') continue;
		if (strcmp(v1[i],v2[i]) == 0) continue;
		match = FALSE;
	}
	freeVals(v1,na); freeVals(v2,na);
	return match;
}

// puts printable version of tuple in user-supplied buffer

void tupleString(Tuple t, char *buf)
{
	strcpy(buf,t);
}
