// using: get_page(), get_record(), ...

Record get_record(Relation rel, RecordId rid)
{
	(pid, tid) = rid
	Page *buf = get_page(rel, pid)
	Record rec = get_record(buf, tid)
	return rec
}