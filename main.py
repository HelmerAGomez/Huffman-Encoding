import heapq
class freqNode:
	def __init__(self, char = None, freq = None):
		self.char = char
		self.freq = freq
		self.left = None
		self.right = None
	def __lt__(self, other):
		return self.freq < other.freq
def frequencyMap(filename):
	letterMap = {}
	contentOfFile = open(filename)
	for line in contentOfFile:
		for letter in line:
			letterMap[letter] = 1 + letterMap.get(letter, 0)
	letterMap['EOF'] = 1 
	contentOfFile.close()
	return letterMap
	
def encodingTree(letterMap):
	pq = []
	for char, freq in letterMap.items():
		heapq.heappush(pq, freqNode(char, freq))
	while len(pq) > 1:
		leftNode = heapq.heappop(pq)
		rightNode = heapq.heappop(pq)
		sumNode = leftNode.freq + rightNode.freq
		newHeadNode = freqNode(None, sumNode)
		newHeadNode.left = leftNode
		newHeadNode.right = rightNode
		heapq.heappush(pq, newHeadNode)
	treeHead = heapq.heappop(pq)
	return treeHead
def addingCode(currNode, map, path = ""):
	if currNode is None:
		return
	if currNode.char is not None:
		map[currNode.char] = path
	addingCode(currNode.left, map, path + '0')
	addingCode(currNode.right, map, path + '1')
def encodingMap(treeHead):
	map = {}
	addingCode(treeHead, map)
	return map
def encodingText(encodeMap,filename):
	codeString = ""
	contentOfFile = open(filename)
	for line in contentOfFile:
		for letter in line:
			codeString += encodeMap[letter]
	codeString += encodeMap['EOF']
	contentOfFile.close()
	numOfPaddingZeros= 8 - (len(codeString) % 8)
	codeString += '0' * numOfPaddingZeros
	
	BinaryFile = open("encodedFile.bin", "wb")
	bytesCode = int(codeString, 2)
	BinaryFile.write(bytesCode.to_bytes(len(codeString) // 8, 'big'))
	BinaryFile.close()
def decodingText(filename, treeHead):
	encryptedFile = open(filename, "rb")
	byte = encryptedFile.read(1)
	codeString = ""
	while byte:
		codeString += f"{ord(byte):08b}"
		byte = encryptedFile.read(1)
	encryptedFile.close()
	currNode = treeHead
	currString = ""
	for currBit in codeString:
		currString += currBit
		currNode = currNode.right if currBit == '1' else currNode.left
		if currNode.char is not None:
			if currNode.char == 'EOF':
				return
			print(currNode.char, end = '')
			currString = ""
			currNode = treeHead
def main():
	print("Enter file name to encode: ")
	filename = input()
	codedFilename = "encodedFile.bin"
	letterMap = frequencyMap(filename)
	treeHead = encodingTree(letterMap)
	encodeMap = encodingMap(treeHead) 
	encodingText(encodeMap, filename)
	decodingText(codedFilename, treeHead)
main()
