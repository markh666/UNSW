-- Assume:a tuple a byte sequence (of data), preceded by a header containing e.g field offsets

-- Fixed-size tuples
-- size = 4 + 8 + 4 + 4 + 8 = 28 bytes + header

create table Course (
	id		integer, -- 4 bytes
	code	char(8), -- 8 bytes, e.g. COMP9315
	uoc		integer, -- 4 bytes
	term	char(4), -- 4 bytes, e.g. "18s2" "19T1"
	avgmark	float,   -- 8 bytes
	primary key (id)
);

-- variable-sized tuples
-- tuple = (header, data)
-- data size = 4 + 8 + ??? + 4 + 8 = 24 + ??? bytes +header

create table Course (
	id		integer, -- 4 bytes
	code	char(8), -- 8 bytes, e.g. COMP 9315
	title	varchar(100), -- ??? bytes
	uoc		integer, -- 4 bytes
	avgmark float, -- 8 bytes
	primary key (id)
);