// Assuming functions...
// Page *get_page(rel, pid)
// Record get_record(p, tid)
// Tuple makeTuple(rel, rec)
// int nTuples(p)
// int nPages(rel)

typedef struct 
{
	Relation rel;
	Page 	*curPage;	// Page buffer
	int		curPID;		// current pid
	int 	curTID;		// current tid
} Scan;

typedef struct 
{
	rel
} ScanData;

typedef ScanData *Scan;

Scan start_scan(Relation rel)
{
	Scan new = malloc(ScanData);
	new->rel = rel;
	new->curPage = get_page(rel, 0);
	new->curPID = 0;
	new->curTID = 0;
	return new;
}

Tuple next_tuple(Scan s)
{
	if (s->curTID == nTuples(s->curPage)) {
		// finished cur page, get next
		if (s->curPID == nPages(s->rel))
			return;
		s->curPID++;
		s->curPage = get_page(s->rel, s->curPID);
		s->curTID = 0;
	}
	Record r = get_record(s->curPage, s->curTID);
	s->curTID++;
	return makeTuple(s->rel, r);
}