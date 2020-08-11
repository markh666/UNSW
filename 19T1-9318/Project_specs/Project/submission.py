import re
import numpy as np

# Merge Two List
def MergeList(listA,listB):
	for i in listB:
		listA.append(i)
	return listA
	
# Use re to split queries
def RegMatchSplit(line):
	L = []
	a = line.split()
	for i in a:
		p = re.split(r"([-,&/()])", i)
		for j in p:
			if j != ' ' and j != '':
				L.append(j)
	return L

# read state file
def ReadState(FilePath):
	NumOfState = 0
	DictOfState = dict()
	DictOfTrans = dict()
	list_tmp = []
	with open(FilePath) as f:  # read file
		while True:  # if not empty
			tmpString = f.readline().rstrip()
			if not tmpString:
				break
			list_tmp.append(tmpString)
	#print('tmpstrng', list_tmp)
	NumOfState = int(list_tmp[0])
	for i in range(NumOfState):
		DictOfState[list_tmp[i + 1]] = i

	list_int = []  # change string to int
	for i in range(NumOfState + 1, len(list_tmp)):
		row = list_tmp[i].split(' ')
		row = list(map(int, row))  # string to int
		list_int.append(row)
	for i in list_int:
		DictOfTrans.setdefault(i[0], {})  # if cannot find the key, then create one
		DictOfTrans[i[0]][i[1]] = i[2]

	return NumOfState, DictOfState, DictOfTrans

# 读取symbol文件
def ReadSymbol(FilePath, NumOfState, DictOfState):
	list_tmp = []
	DictOfSymbol = {}
	DictOfEmit = {}
	EmitMat = np.matrix
	with open(FilePath) as f:  # read file
		while True:  # if not empty
			tmpString = f.readline().rstrip()
			if not tmpString:
				break
			list_tmp.append(tmpString)
	NumOfSymbol = int(list_tmp[0])
	for i in range(NumOfSymbol):
		DictOfSymbol[list_tmp[i + 1]] = i
	list_int = []
	for i in range(NumOfSymbol + 1, len(list_tmp)):
		row = list_tmp[i].split(' ')  # use space to split f1 f2 f3
		row = list(map(int, row))
		list_int.append(row)
	for i in list_int:
		DictOfEmit.setdefault(i[0], {})  # if cannot find the key, then create one
		DictOfEmit[i[0]][i[1]] = i[2]

	return NumOfSymbol, DictOfSymbol, DictOfEmit

# read file and calculate the transition rate
def CalcStateMat(n, DS, DT, s): # input the number of states, DictOfState DictOfTrans s/smooth
	TransMat = np.zeros(shape = (n, n), dtype = float)  # create a matrix to record probability
	IintMat = np.matrix

	Sum = [0] * n   # initial an array
	for i in range(n):
		if i in DT.keys():
			Sum[i] = sum(DT[i].values())

	#print(DT)
	for i in range(n):
		if i != DS['END']:  # if not end
			for j in range(n):
				tmp = Sum[i]+(s*n)-1
				if j == DS['BEGIN']:
					continue
				if j in DT[i].keys():
					if i in DT.keys():
						TransMat[i, j] = (s+DT[i][j])/tmp
				else:
					TransMat[i, j] =s/tmp


	for i in range(n):         # initial an array
		if i == DS['BEGIN']:
			IintMat = TransMat[i, :]

	return TransMat, IintMat

# read symbol 
def CalcSymbolMat(n,m,DS,DE,s):  #input NumOfState,NumOfSymbol,DictOfSymbol,DictOfEmit,smooth
	Sum = [0]*n
	EmitMat = np.zeros(shape = (n, m + 1))

	for i in range(n):
		if i != DS['END'] and i!= DS['BEGIN'] and  i in DE.keys():
			Sum[i] = sum(DE[i].values())

	for i in range(n):
		if DS['END'] != i:
			if DS['BEGIN'] != i:
				for j in range(m + 1):
					tmp = Sum[i] + s * m + 1
					if j in DE[i].keys():
						if  i in DE.keys():
							EmitMat[i, j] = (s+DE[i][j])/(tmp)
					else:
						EmitMat[i, j] = s/(tmp)
	return EmitMat

# create a 3D matrix n*m*t
def MakeMatrix(n,m,t):
	MatDp = []  # Create a 3D matrix, inital the matirx
	for i in range(n):
		MatDp.append([])
		for j in range(m):
			MatDp[i].append([])
			for k in range(t):
				MatDp[i][j].append([])
				MatDp[i][j][k].append(0.0)
				MatDp[i][j][k].append([])
	return MatDp

# use symbol index to initial the matrix
def InitMatrix(MatDp, n, DSt, DSym, IM, EM,Query):  # n/NumOfState  DSt/DictOfState DSym/DictOfSymbol IM/InitMat EM/EmitMat
	MatDp[DSt['BEGIN']][0][0] = [1, []]
	for i in range(n):
		if Query[0] not in DSym.keys():
			MatDp[i][1][0][1].append(DSt['BEGIN'])

	for i in range(n):
		if Query[0] in DSym.keys():
			MatDp[i][1][0][0] = EM[i, DSym[Query[0]]] * IM[i]
		else:
			MatDp[i][1][0][0] = EM[i, DSym['UNK']] * IM[i]

	return MatDp

#	start calculate the probability and path
def CalcMatrix(MatDp,lens,NumOfState,DSym,DSt,TM,EM,Query,k): #DSym/DictOfSymbol DSt/DictOfState TM/TransMat EM/EmitMat
	EndMat=[]
	for j in range(2, lens + 1):
		for i in range(NumOfState):
			lists = []
			if j > lens + 1:
				continue
			else:
				EndMat = TM[:, DSt['END']]
			for m in range(NumOfState):
				for t in range(k):  # record the symbol
					tmp1 = MatDp[m][j - 1][t][0] * TM[m, i]
					tmp2 = MatDp[m][j - 1][t][1] + [m]
					if i < NumOfState +1:
						if Query[j-1] in DSym.keys():
							lists.append((tmp1*EM[i,DSym[Query[j-1]]],tmp2))
						else:
							lists.append((tmp1*EM[i,DSym['UNK']],tmp2))
					elif i < NumOfState +lens:
						if Query[j-1] in DSym.keys():
							lists.append((tmp1*EM[i,DSym[Query[j-1]]],tmp2))
						else:
							print("Error")
							raise Exception
					else:
						print("Error")
						raise Exception

			lists.sort(key=lambda p: p[0], reverse=True)# sort the list
			for n in range(k):
				MatDp[i][j][n][0] = lists[n][0]
				MatDp[i][j][n][1] = MergeList(MatDp[i][j][n][1],lists[n][1])


	for i in range(NumOfState):
		for j in range(k):
			MatDp[i][lens + 1][j][0] = MatDp[i][lens][j][0]*EndMat[i]
			MatDp[i][lens + 1][j][1] = MergeList(MatDp[i][lens + 1][j][1],MatDp[i][lens][j][1] + [i])
	return MatDp

# Merge the result
def MergeMatrix(MatDp,lens,DS,n,k): #DS/DictOfState n/NumOfState
	re = []
	result = []
	Rresult = []
	EndId = DS['END']
	for i in range(n):
		re = MergeList(re,MatDp[i][lens+ 1])
	re.sort(key=lambda x: x[0], reverse=True)
	for i in range(k):
		result = re[i][1] + [EndId] + [np.log(re[i][0])]
		if result[0] != DS['BEGIN']:
			result.insert(0, DS['BEGIN'])
		Rresult.append(result)
	return Rresult

#hmm algorithm
def ViterbiAlgo(NumOfState, NumOfSymbol, DictOfState, DictOfSymbol, TransMat, EmitMat, InitMat, Query, t): #t is the thrid d of matrix
	lens = len(Query)
	MatDp = MakeMatrix(NumOfState,lens+2,t)   #initial a matrix  n*m*t
	MatDp = InitMatrix(MatDp,NumOfState,DictOfState,DictOfSymbol,InitMat,EmitMat,Query)   # initial the matrix according the symbol
	MatDp = CalcMatrix(MatDp,lens,NumOfState,DictOfSymbol,DictOfState,TransMat,EmitMat,Query,t) # calculate
	re = MergeMatrix(MatDp,lens,DictOfState,NumOfState,t)      # merge the result and change the probablity to log format
	return re

# Question 1
def viterbi_algorithm(State_File, Symbol_File, Query_File):  # do not change the heading of the function
	Result = []
	# read the file
	NumOfState, DictOfState, DictOfTrans = ReadState(State_File)
	NumOfSymbol, DictOfSymbol, DictOfEmit = ReadSymbol(Symbol_File, NumOfState, DictOfState)

	#	make the matrix
	TransMat, InitMat = CalcStateMat(NumOfState, DictOfState, DictOfTrans, 1)
	EmitMat = CalcSymbolMat(NumOfState, NumOfSymbol, DictOfState, DictOfEmit, 1)

	with open(Query_File) as f:
		while True:
			string = f.readline().rstrip()  # read query and split each word
			if not string:  # don't need to record space
				break
			Query = RegMatchSplit(string)           # use re to split
			DictOfSymbol["UNK"] = NumOfSymbol  # define for UNK 
			list_tmp = ViterbiAlgo(NumOfState, NumOfSymbol, DictOfState, DictOfSymbol, TransMat, EmitMat, InitMat, Query, 1)
			Result = MergeList(Result,list_tmp)

	return Result

# Question 2
def top_k_viterbi(State_File, Symbol_File, Query_File, k):  # do not change the heading of the function
	result = []

	# read the file
	NumOfState, DictOfState, DictOfTrans = ReadState(State_File)
	NumOfSymbol, DictOfSymbol, DictOfEmit = ReadSymbol(Symbol_File, NumOfState, DictOfState)

	#	make the matrix
	TransMat, InitMat = CalcStateMat(NumOfState, DictOfState, DictOfTrans, 1)
	EmitMat = CalcSymbolMat(NumOfState, NumOfSymbol, DictOfState, DictOfEmit, 1)

	with open(Query_File) as f:
		while True:
			string = f.readline().rstrip()
			if not string:
				break
			Query = RegMatchSplit(string)
			# print('query', query)
			DictOfSymbol["UNK"] = NumOfSymbol
			list_tmp = ViterbiAlgo(NumOfState, NumOfSymbol, DictOfState, DictOfSymbol, TransMat, EmitMat, InitMat,Query, k)
			result = MergeList(result,list_tmp)

	return result

# Question 3 + Bonus
def advanced_decoding(State_File, Symbol_File, Query_File):  # do not change the heading of the function
	#NumOfState, NumOfSymbol, DictOfState, DictOfSymbol, TransMat, EmitMat, InitMat = file_reader(State_File,Symbol_File,True)
	# read the file
	NumOfState, DictOfState, DictOfTrans = ReadState(State_File)
	NumOfSymbol, DictOfSymbol, DictOfEmit = ReadSymbol(Symbol_File, NumOfState, DictOfState)

	#	make the matrix
	TransMat, InitMat = CalcStateMat(NumOfState, DictOfState, DictOfTrans, 0.0001)
	EmitMat = CalcSymbolMat(NumOfState, NumOfSymbol, DictOfState, DictOfEmit, 0.0001)

	result = []
	with open(Query_File) as f:
		while True:
			string = f.readline().rstrip()
			if not string:
				break
			Query = RegMatchSplit(string)
			DictOfSymbol["UNK"] = NumOfSymbol
			list_tmp = ViterbiAlgo(NumOfState, NumOfSymbol, DictOfState, DictOfSymbol, TransMat, EmitMat, InitMat,Query, 1)
			result = MergeList(result,list_tmp)

	return result
