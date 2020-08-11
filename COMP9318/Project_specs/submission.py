import re
import numpy as np

#合并两个list
def MergeList(listA,listB):
	for i in listB:
		listA.append(i)
	return listA
#给定字符串 进行正则表达式分割
def RegMatchSplit(line):
	L = []
	a = line.split()
	for i in a:
		p = re.split(r"([-,&/()])", i)
		for j in p:
			if j != ' ' and j != '':
				L.append(j)
	# print(L)
	return L
#读取state文件
def ReadState(FilePath):
	NumOfState = 0
	DictOfState = dict()
	DictOfTrans = dict()
	list_tmp = []
	with open(FilePath) as f:  # 首先将文件都读取到文本中
		while True:  # 如果文件不为空就一直读取
			tmpString = f.readline().rstrip()
			if not tmpString:
				break
			list_tmp.append(tmpString)
	#print('tmpstrng', list_tmp)
	NumOfState = int(list_tmp[0])
	for i in range(NumOfState):
		DictOfState[list_tmp[i + 1]] = i

	list_int = []  # 将string转换为int
	for i in range(NumOfState + 1, len(list_tmp)):
		row = list_tmp[i].split(' ')
		row = list(map(int, row))  # 字符串转为int
		list_int.append(row)
	for i in list_int:
		DictOfTrans.setdefault(i[0], {})  # 如果没有对应的key就新建一个
		DictOfTrans[i[0]][i[1]] = i[2]

	return NumOfState, DictOfState, DictOfTrans
# 读取symbol文件
def ReadSymbol(FilePath, NumOfState, DictOfState):
	list_tmp = []
	DictOfSymbol = {}
	DictOfEmit = {}
	EmitMat = np.matrix
	with open(FilePath) as f:  # 首先将文件都读取到文本中
		while True:  # 如果文件不为空就一直读取
			tmpString = f.readline().rstrip()
			if not tmpString:
				break
			list_tmp.append(tmpString)
	NumOfSymbol = int(list_tmp[0])
	for i in range(NumOfSymbol):
		DictOfSymbol[list_tmp[i + 1]] = i
	list_int = []
	for i in range(NumOfSymbol + 1, len(list_tmp)):
		row = list_tmp[i].split(' ')  # 使用空格分割f1,f2,f3
		row = list(map(int, row))
		list_int.append(row)
	for i in list_int:
		DictOfEmit.setdefault(i[0], {})  # 如果DictOfEmit 字典中没有对应的key就新建一个
		DictOfEmit[i[0]][i[1]] = i[2]

	return NumOfSymbol, DictOfSymbol, DictOfEmit
#读取state文件后计算矩阵
def CalcStateMat(n, DS, DT, s): #输入参数为 n/state行数 DictOfState DictOfTrans s/smooth平滑值
	TransMat = np.zeros(shape = (n, n), dtype = float)  # 设置一个  n*n的矩阵
	IintMat = np.matrix

	Sum = [0] * n   #首先初始化一个数组
	for i in range(n):
		if i in DT.keys():
			Sum[i] = sum(DT[i].values())

	#print(DT)
	for i in range(n):
		if i != DS['END']:  # 如果此时不是结束
			for j in range(n):
				tmp = Sum[i]+(s*n)-1
				if j == DS['BEGIN']:
					continue
				if j in DT[i].keys():
					if i in DT.keys():
						TransMat[i, j] = (s+DT[i][j])/tmp
				else:
					TransMat[i, j] =s/tmp


	for i in range(n):         #初始化init数组
		if i == DS['BEGIN']:
			IintMat = TransMat[i, :]

	return TransMat, IintMat
#读取symbol文件
def CalcSymbolMat(n,m,DS,DE,s):  #输入参数为 NumOfState,NumOfSymbol,DictOfSymbol,DictOfEmit,smooth
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
#构造一个矩阵  n*m*t
def MakeMatrix(n,m,t):
	MatDp = []  # 定义dp矩阵  首席按初始化一个三维的空矩阵  将开始设为1  其他都设为0
	for i in range(n):
		MatDp.append([])
		for j in range(m):
			MatDp[i].append([])
			for k in range(t):
				MatDp[i][j].append([])
				MatDp[i][j][k].append(0.0)
				MatDp[i][j][k].append([])
	return MatDp
# 根据symbol符号初始化矩阵
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
#进行计算
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
				for t in range(k):  # 如果该符号存在 就加入  否则不加入
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

			lists.sort(key=lambda p: p[0], reverse=True)#进行排序
			for n in range(k):
				MatDp[i][j][n][0] = lists[n][0]
				MatDp[i][j][n][1] = MergeList(MatDp[i][j][n][1],lists[n][1])


	for i in range(NumOfState):
		for j in range(k):
			MatDp[i][lens + 1][j][0] = MatDp[i][lens][j][0]*EndMat[i]
			MatDp[i][lens + 1][j][1] = MergeList(MatDp[i][lens + 1][j][1],MatDp[i][lens][j][1] + [i])
	return MatDp
#合并结果
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
#hmm算法实现
def ViterbiAlgo(NumOfState, NumOfSymbol, DictOfState, DictOfSymbol, TransMat, EmitMat, InitMat, Query, t): #t是三维矩阵的第三维维度
	lens = len(Query)
	MatDp = MakeMatrix(NumOfState,lens+2,t)   #首先初始化一个三维矩阵  n*m*t
	MatDp = InitMatrix(MatDp,NumOfState,DictOfState,DictOfSymbol,InitMat,EmitMat,Query)   #根据symbol情况初始化矩阵
	MatDp = CalcMatrix(MatDp,lens,NumOfState,DictOfSymbol,DictOfState,TransMat,EmitMat,Query,t) #进行计算
	re = MergeMatrix(MatDp,lens,DictOfState,NumOfState,t)      #最后合并结果 log计算
	return re

# Question 1
def viterbi_algorithm(State_File, Symbol_File, Query_File):  # do not change the heading of the function
	Result = []
	#首先读取文件
	NumOfState, DictOfState, DictOfTrans = ReadState(State_File)
	NumOfSymbol, DictOfSymbol, DictOfEmit = ReadSymbol(Symbol_File, NumOfState, DictOfState)

	#然后读取信息构造矩阵
	TransMat, InitMat = CalcStateMat(NumOfState, DictOfState, DictOfTrans, 1)
	EmitMat = CalcSymbolMat(NumOfState, NumOfSymbol, DictOfState, DictOfEmit, 1)

	with open(Query_File) as f:
		while True:
			string = f.readline().rstrip()  # 打开文件并删除文件末尾的空格
			if not string:  # 如果字符串空 就跳出循环
				break
			Query = RegMatchSplit(string)           #使用正则表达式分割出所有的state
			DictOfSymbol["UNK"] = NumOfSymbol  # 为未知符号标定序号
			list_tmp = ViterbiAlgo(NumOfState, NumOfSymbol, DictOfState, DictOfSymbol, TransMat, EmitMat, InitMat, Query, 1)
			Result = MergeList(Result,list_tmp)

	return Result
# Question 2
def top_k_viterbi(State_File, Symbol_File, Query_File, k):  # do not change the heading of the function
	result = []

	# 首先读取文件
	NumOfState, DictOfState, DictOfTrans = ReadState(State_File)
	NumOfSymbol, DictOfSymbol, DictOfEmit = ReadSymbol(Symbol_File, NumOfState, DictOfState)

	# 然后读取信息构造矩阵
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
	# 首先读取文件
	NumOfState, DictOfState, DictOfTrans = ReadState(State_File)
	NumOfSymbol, DictOfSymbol, DictOfEmit = ReadSymbol(Symbol_File, NumOfState, DictOfState)

	# 然后读取信息构造矩阵
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


# StateFile = 'D:/Administrator/desktop_bak/Desktop/Project/Project/dev_set/State_File'
# SymbolFile = 'D:/Administrator/desktop_bak/Desktop/Project/Project/dev_set/Symbol_File'
# QueryFile = 'D:/Administrator/desktop_bak/Desktop/Project/Project/dev_set/Query_File'

# #测试语句
# viterbi_algorithm(StateFile, SymbolFile, QueryFile)
# #top_k_viterbi(StateFile, SymbolFile, QueryFile, 3)  #此处的3填上对应的 top k
# #advanced_decoding(StateFile, SymbolFile, QueryFile)
# StateFile1 = 'dev_set/State_File'
# SymbolFile1 = 'dev_set/Symbol_File'
# QueryFile1 = 'dev_set/Query_File'



# result = viterbi_algorithm(StateFile1, SymbolFile1, QueryFile1)
# # print(re1)

# f = open('result.txt', 'w')
# for i in result:
# 	r= '['
# 	for j in i:
# 		r += str(j)
# 		if j < 0:
# 			r += ']\n'
# 		else:
# 			r += ', '
# 	f.write(r)
# f.close()

# # check the difference number for correct labels
# a = open('Q1Ans.txt', 'r')
# r = open('result.txt', 'r')
# count = 0
# total = 0
# a_line = a.readline()
# r_line = r.readline()
# while a_line:
# 	total += 1
# 	A = a_line.split()
# 	R = r_line.split()
# 	if A != R:
# 		count += 1
# 		print('Expect:', A)
# 		print('Got:', R)
# 		print(total)
# 	a_line = a.readline()
# 	r_line = r.readline()
# print(count)
# print(total)