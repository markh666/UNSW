//******************************************************************************
//COMP9315 Database Systems Imp 
//Assignment 1 Adding an Email Data Type to PostgreSQL
//******************************************************************************
#include "postgres.h"
#include "fmgr.h"
#include "libpq/pqformat.h"		
#include <string.h>
#include <ctype.h>

PG_MODULE_MAGIC;

typedef struct _email {
   int32 length;
   char address[FLEXIBLE_ARRAY_MEMBER];
}  EmailAddr;

//* Since we use V1 function calling convention, all these functions have
//* the same signature as far as C is concerned.  We provide these prototypes
//* just to forestall warnings when compiled with gcc -Wmissing-prototypes.

Datum	email_in(PG_FUNCTION_ARGS);     // input
Datum	email_out(PG_FUNCTION_ARGS);    // output
Datum	email_lt(PG_FUNCTION_ARGS);     // EmailAdd1 < EmailAdd2
Datum	email_le(PG_FUNCTION_ARGS);     // EmailAdd1 <= EmailAdd2
Datum	email_eq(PG_FUNCTION_ARGS);     // EmailAdd1 == EmailAdd2 
Datum	email_neq(PG_FUNCTION_ARGS);    // EmailAdd1 <> EmailAdd2 
Datum	email_gt(PG_FUNCTION_ARGS);     // EmailAdd1 > EmailAdd2 
Datum	email_ge(PG_FUNCTION_ARGS);     // EmailAdd1 >= EmailAdd2
Datum	email_deq(PG_FUNCTION_ARGS);    // EmailAdd1 & EmailAdd2 has same domain
Datum   email_ndeq(PG_FUNCTION_ARGS);   // EmailAdd1 & EmailAdd2 has different domain
Datum	email_cmp(PG_FUNCTION_ARGS);    // compare two email address
Datum   email_hval(PG_FUNCTION_ARGS);   // hash function
bool    isValidInput(char *str);        // under RFC822 address standards

//*****************************************************************************
//* Input/Output functions
//*****************************************************************************

PG_FUNCTION_INFO_V1(email_in);

// store the email type data
Datum email_in(PG_FUNCTION_ARGS)
{
    char *str;
    EmailAddr *result;
    str = PG_GETARG_CSTRING(0);
    int i;
    //change address to connical form
    for (i = 0; str[i]; i++) {
        str[i] = tolower(str[i]);
    }
    
    // report invalid error
    if ( !isValidInput(str) ) {
        ereport( ERROR, (errcode (ERRCODE_INVALID_TEXT_REPRESENTATION),
                  errmsg ("invalid: \"%s\"", str)));
    }

    // Allocate memory
    result =(EmailAddr *) palloc(sizeof(int32)+1+strlen(str));
    SET_VARSIZE(result,sizeof(int32)+1+strlen(str));    // store the total size of the datum
    strcpy(result->address,str);    // copy email address to result
    PG_RETURN_POINTER(result);
}

// check email address is valid or not
bool isValidInput(char *str) {
    int  i           = 0;
    int  at          = 0;
    int  domainWords = 0;
    char prev        = str[0];
    bool domain      = false;
    int domain_len = 0;
    int local_len = 0;
 
    prev = str[0];

    // the first word must be a letter
    if ( !isalpha(str[0]) ) { 
        return false;
    }

    for (i = 0; str[i]; i++) {
        //check char is in range [a-z] && [0-9] && '-' && '@' && '.'
        if ( !(isalpha(str[i]) || isdigit(str[i]) || str[i] == '-'   || str[i] == '@'   || str[i] == '.') ) {
            //printf ("isalpha = %d, isdigit = %d, is '-' = %d\ninvalid = true\n", isalpha(str[i]), isdigit(str[i]), (str[i]=='-'));
            return false;
        }

        //check word begins with letter
        //takes care of empty words (e.g. j..shepherd@funny.email.com)
        if ((prev == '.' || prev == '@') && !isalpha(str[i])) { 
            printf("%c isn't [a-z]\n", str[i]); 
            return false;
        }

        //check word ends with letter or digit
        if ((str[i] == '.' || str[i] == '@' || i == strlen(str) ) && !(isalpha(prev) || isdigit(prev))) { 
            if (prev != '@') {
                //printf("last letter of word (%c) isn't [a-z] || [0-9]\n", prev); 
                return false;
            }
        }

        //check only one '@' in str 
        if (str[i] == '@') { 
            at++;
            domain = true;
            if (at > 1) { 
                //printf ("too many @ (%d)", at); 
                return false;
            }  
        }

        // record the length of address
        if (at == 0 && str[i]!='@') {
            local_len ++;
            if (local_len >256) {
                return false;
            }
        }
        // both local and domain address cannot exceed 256
        if (at != 0 && str[i]!='@') {
            domain_len ++;
            if (domain_len > 256) {
                return false;
            }
        }

        //check domain contains at least 2 words
        if (domain && (prev == '.' || prev == '@')) {
             domainWords++;
        }
        prev = str[i];
    }

    if (domainWords < 2) { 
        //printf("not enough words in domain of %s (%d)\n", str, domainWords); 
        return false;
    }

  return true;
}

PG_FUNCTION_INFO_V1(email_out);
// output email address
Datum email_out(PG_FUNCTION_ARGS)
{
    EmailAddr    *email = (EmailAddr *) PG_GETARG_POINTER(0);
    char     *result;
    
    result = psprintf("%s", email->address);
    PG_RETURN_CSTRING(result);
}

//*****************************************************************************
//* Operator class for defining B-tree index
//*****************************************************************************

// compare email address function
static int email_cmp_internal(EmailAddr *a, EmailAddr *b)
{
    char *adomain,*bdomain,*alocal,*blocal;
    char aadd[strlen(a->address)+2],badd[strlen(b->address)+2]; 
    int i;
    memset(aadd,0,sizeof(aadd));
    memset(badd,0,sizeof(badd));
    //change address *a to connical form
    for (i = 0; i<strlen(a->address); i++) {
        aadd[i] = tolower(a->address[i]);
    }
    //change address *b to connical form
    for (i = 0; i<strlen(b->address); i++) {
        badd[i] = tolower(b->address[i]);    
    }	
    // slice local address and domain address
    alocal = strtok(aadd, "@");
    adomain = strtok(NULL, "@");
    blocal = strtok(badd, "@");
    bdomain = strtok(NULL, "@");

    // decide the order
    if (strcmp(adomain, bdomain) != 0 ) {
	    return strcmp(adomain, bdomain);
	}

	if (strcmp(alocal, blocal) != 0 ) {
	    return strcmp(alocal, blocal);
	}
    return 0;   // same email address
	//return strcmp(&a, &b);
}

// email address to hash function
static int email_hash_internal(EmailAddr *a)
{
    char *aaddress;
    char aadd[strlen(a->address)+2]; 
    int i;
	int32 h1 = 0;
    memset(aadd,0,sizeof(aadd));
    //change address *a to connical form
    for (i = 0; i<strlen(a->address); i++) {
        aadd[i] = tolower(a->address[i]);
    }
    for(aaddress=aadd; *aaddress; aaddress++){
	  h1 = h1*31 + *aaddress;
    }

    return h1;
}

// email a < email b
PG_FUNCTION_INFO_V1(email_lt);

Datum email_lt(PG_FUNCTION_ARGS)
{
	EmailAddr    *a = (EmailAddr *) PG_GETARG_POINTER(0);
	EmailAddr    *b = (EmailAddr *) PG_GETARG_POINTER(1);

	PG_RETURN_BOOL(email_cmp_internal(a, b) < 0);
}

// email a <= email b
PG_FUNCTION_INFO_V1(email_le);

Datum email_le(PG_FUNCTION_ARGS)
{
	EmailAddr    *a = (EmailAddr *) PG_GETARG_POINTER(0);
	EmailAddr    *b = (EmailAddr *) PG_GETARG_POINTER(1);

	PG_RETURN_BOOL(email_cmp_internal(a, b) <= 0);
}

// email a == email b
PG_FUNCTION_INFO_V1(email_eq);

Datum email_eq(PG_FUNCTION_ARGS)
{
	EmailAddr    *a = (EmailAddr *) PG_GETARG_POINTER(0);
	EmailAddr    *b = (EmailAddr *) PG_GETARG_POINTER(1);

	PG_RETURN_BOOL(email_cmp_internal(a, b) == 0);
}

// email a != email b
PG_FUNCTION_INFO_V1(email_neq);

Datum email_neq(PG_FUNCTION_ARGS)
{
	EmailAddr    *a = (EmailAddr *) PG_GETARG_POINTER(0);
	EmailAddr    *b = (EmailAddr *) PG_GETARG_POINTER(1);

	PG_RETURN_BOOL(email_cmp_internal(a, b) != 0);
}

// email a >= email b
PG_FUNCTION_INFO_V1(email_ge);

Datum email_ge(PG_FUNCTION_ARGS)
{
	EmailAddr    *a = (EmailAddr *) PG_GETARG_POINTER(0);
	EmailAddr    *b = (EmailAddr *) PG_GETARG_POINTER(1);

	PG_RETURN_BOOL(email_cmp_internal(a, b) >= 0);
}

// email a > email b
PG_FUNCTION_INFO_V1(email_gt);

Datum email_gt(PG_FUNCTION_ARGS)
{
	EmailAddr    *a = (EmailAddr *) PG_GETARG_POINTER(0);
	EmailAddr    *b = (EmailAddr *) PG_GETARG_POINTER(1);

	PG_RETURN_BOOL(email_cmp_internal(a, b) > 0);
}

// email a (domain) = email b (domain)
PG_FUNCTION_INFO_V1(email_deq);

Datum email_deq(PG_FUNCTION_ARGS)
{
	EmailAddr    *a = (EmailAddr *) PG_GETARG_POINTER(0);
	EmailAddr    *b = (EmailAddr *) PG_GETARG_POINTER(1);
    int i;
    char *adomain,*bdomain,*alocal,*blocal;
    char aadd[strlen(a->address)+2],badd[strlen(b->address)+2];
    memset(aadd,0,sizeof(aadd));
    memset(badd,0,sizeof(badd));

    //change address *a to connical form
    for (i = 0; i<strlen(a->address); i++) {
        aadd[i] = tolower(a->address[i]);    
    }
    //change address *b to connical form
    for (i = 0; i<strlen(b->address); i++) {
        badd[i] = tolower(b->address[i]);
    }	
    // slice local address and domain address
    alocal = strtok(aadd, "@");
    adomain = strtok(NULL, "@");
    blocal = strtok(badd, "@");
    bdomain = strtok(NULL, "@");

	PG_RETURN_BOOL(strcmp(adomain, bdomain) == 0);
}

// email a (domain) != email b (domain)
PG_FUNCTION_INFO_V1(email_ndeq);

Datum email_ndeq(PG_FUNCTION_ARGS)
{
	EmailAddr    *a = (EmailAddr *) PG_GETARG_POINTER(0);
	EmailAddr    *b = (EmailAddr *) PG_GETARG_POINTER(1);
    char *adomain,*bdomain,*alocal,*blocal;
    char aadd[strlen(a->address)+2],badd[strlen(b->address)+2]; 
    int i;
    memset(aadd,0,sizeof(aadd));
    memset(badd,0,sizeof(badd));
    //change address *a to connical form
    for (i = 0; i<strlen(a->address); i++) {
        aadd[i] = tolower(a->address[i]);
    }
    //change address *a to connical form
    for (i = 0; i<strlen(b->address); i++) {
        badd[i] = tolower(b->address[i]);
    }	
    // slice local address and domain address
    alocal = strtok(aadd, "@");
    adomain = strtok(NULL, "@");
    blocal = strtok(badd, "@");
    bdomain = strtok(NULL, "@");

	PG_RETURN_CSTRING(strcmp(adomain, bdomain) != 0);
}

// support function
PG_FUNCTION_INFO_V1(email_cmp);
Datum email_cmp(PG_FUNCTION_ARGS)
{
	EmailAddr    *a = (EmailAddr *) PG_GETARG_POINTER(0);
	EmailAddr    *b = (EmailAddr *) PG_GETARG_POINTER(1);

	PG_RETURN_INT32(email_cmp_internal(a, b));
}

// support function
PG_FUNCTION_INFO_V1(email_hval);
Datum email_hval(PG_FUNCTION_ARGS)
{
	EmailAddr    *a = (EmailAddr *) PG_GETARG_POINTER(0);

	PG_RETURN_INT32(email_hash_internal(a));
}
