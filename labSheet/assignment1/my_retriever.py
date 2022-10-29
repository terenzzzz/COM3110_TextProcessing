# Do we need to process the query
# Index mean in engine
# Query mean in engine
# The return in for_query
# Goal: Find The Best 10 Document  for each queries?
# What method to rank (queries has many words) term_weighting???

#index: {'santa': {3204: 1}, ..., 'monica': {3204: 1}}
# (1, ['articles', 'exist', 'deal', 'tss', 'time', 'sharing', 'system', 'operating', 'system', 'ibm', 'computers'])
import math
class Retrieve:
    
    # Create new Retrieve object storing index and term weighting
    # scheme. (You can extend this method, as required.)
    def __init__(self, index, term_weighting):
        self.index = index
        self.term_weighting = term_weighting
        self.num_docs = self.compute_number_of_documents()
        print('Running in ',self.term_weighting)
        print('Total docs: ',self.num_docs)
        # print(len(self.index))

        
    def compute_number_of_documents(self):
        self.doc_ids = set() 
        for term in self.index:
            self.doc_ids.update(self.index[term])
        return len(self.doc_ids)
    

    # Method performing retrieval for a single query (which is 
    # represented as a list of preprocessed terms). Returns list 
    # of doc ids for relevant docs (in rank order).
    
    def for_query(self, query):
        qDSum = []
        fullList = {}
        quertSet=set()
        for q in query:
            quertSet.add(q)
        # print('quertSet: ', quertSet)
        
        if self.term_weighting == 'binary':
            docDict={}
            for docId in self.doc_ids:
                docDict[docId] = {}
                for k in query:
                    if k in self.index:
                        if docId in self.index[k]:
                            binaryNum = 1
                        else:
                            binaryNum = 0
                        docDict[docId][k] = binaryNum
            
                    
            # 筛选出相关的文章
            candidate = {}
            for doc in docDict:
                valueList = list(docDict[doc].values())
                for val in valueList:
                    if val == 1:
                        candidate[doc]= docDict[doc]
            print(candidate)
                        
            # 计算
            # 分母
            docSize = {}
            for term in self.index:
                for docId in self.index[term]:
                    if docId in docSize:
                        docSize[docId] += 1
                    else:
                        docSize[docId] = 0

            # 分子
            result = {}
            for doc in candidate:
                valueList = list(candidate[doc].values())
                pwdPSum=docSize[doc]
                pQSum=0
                for val in valueList:
                    if val == 1:
                        pQSum += 1
                cosVal = pQSum/math.sqrt(pwdPSum)
                result[doc] = cosVal
            # print(result)
            
            # 排序
            top_10 = []
            sort = sorted(result.items(),key=lambda x:x[1])[:10]
            for docId,sim in sort:
                top_10.append(docId)
                    
        
        return top_10

    # def compute_size_of_document_vector(self,file):
        
