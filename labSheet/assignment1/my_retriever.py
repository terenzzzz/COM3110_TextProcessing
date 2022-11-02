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

    def compute_number_of_documents(self):
        self.doc_ids = set() 
        for term in self.index:
            self.doc_ids.update(self.index[term])
        return len(self.doc_ids)
    

    # Method performing retrieval for a single query (which is 
    # represented as a list of preprocessed terms). Returns list 
    # of doc ids for relevant docs (in rank order).
    
    def for_query(self, query):
        # 调用processQuery处理query
        query = self.processQuery(query)
        
#==============================================================================       
        
        docVector={} # 包含特定模式数据的字典
        result = {} # 返回十个最相关文件的id
            
#==============================================================================
# Binary Mode
        if self.term_weighting == 'binary':
            # 判断query词是否出现在document中
            for docId in self.doc_ids:
                docVector[docId] = {}
                for k in query:
                    if k in self.index:
                        if docId in self.index[k]:
                            binaryNum = 1
                        else:
                            binaryNum = 0
                        docVector[docId][k] = binaryNum
            # 调用相似度计算返回结果
            result = self.simCalc_binary(docVector)
            
#==============================================================================                    
# TF(Term Frequency) Mode

        elif self.term_weighting == 'tf':
            # 计算关键词出现在每篇文章中的次数
            docVector = self.tfCalc(query)
            
            # 调用相似度计算返回结果
            result = self.simCalc_tf(docVector, query)
            
#==============================================================================    
# TF.IDF

        else:
            # 计算关键词在每篇文章中出现的次数(tf)
            tfDict = self.tfCalc(query)
            
            # size od Collection(|D|)
            collectionSize = self.num_docs
            
            # 计算idf
            idfDict = self.idfCalc(query,collectionSize)

            # 计算tfIdf
            tfIdfDict = self.tfIdfCalc(query,tfDict,idfDict)
            
            
            # 筛选出有相关的
            docVector = {}
            for docId in tfIdfDict:
                for tfidf in tfIdfDict[docId].values():
                    if tfidf > 0:
                        docVector[docId] = tfIdfDict[docId]
                        
            result = self.simCalc_tfIdf(query,idfDict,docVector)
            
#==============================================================================
# Return 

        # 调用排序返回相似度最大的十个
        return self.rankTop(result,10)

#==============================================================================
# Calculation
    # 相似度计算(Binary)
    def simCalc_binary(self,docDict):
        result = {}
        # 计算文件里有多少个Term
        docSize = {}
        for term in self.index:
            for docId in self.index[term]:
                if docId in docSize:
                    docSize[docId] += 1
                else:
                    docSize[docId] = 0
                    
        # 计算有多少词语又在文件中 又在query中
        for doc in docDict:
            valueList = list(docDict[doc].values())
            pwdDSum = docSize[doc]
            qdSum=0
            for val in valueList:
                if val == 1:
                    qdSum += 1
            # 通过计算cos获取sim值
            cosVal = qdSum / math.sqrt(pwdDSum)
            result[doc] = cosVal
        return result
    
    # 相似度计算(TF)
    def simCalc_tf(self,docDict,query):
        result = {}
        # 分母
        pwdDSum = {}
        for term in self.index:
            for docId in self.index[term]:
                if docId in pwdDSum:
                    pwdDSum[docId] += self.index[term][docId] * self.index[term][docId]
                else:
                    pwdDSum[docId] = self.index[term][docId] * self.index[term][docId]
               
        # 分子 qd
        for docId in docDict:
            qdSum = 0
            for term in docDict[docId]:
                d = docDict[docId][term]
                q = query[term]
                qdSum += d * q
            # 通过计算cos获取sim值
            cosVal = qdSum / math.sqrt(pwdDSum[docId])
            result[docId] = cosVal
        return result
    
    def simCalc_tfIdf(self,query,idfDict,docVector):
        result = {}
        
        # 计算query中的tfidf值
        queryTfIdf = self.q_tfIdfCalc(query,idfDict)
        
                
        # 计算sim
        result = {}
        for docId in docVector:
            qdSum = 0
            pwdDSum = 0
            for k in docVector[docId]:
                q = queryTfIdf[k]
                d = docVector[docId][k]
                qdSum += q * d
                pwdDSum += d * d
            cosVal = qdSum / math.sqrt(pwdDSum)
            result[docId] = cosVal
           
        return result
    
    
#==============================================================================
# Helper

    # 计算Term Frequency
    def tfCalc(self,query):
        # 计算关键词在每篇文章中出现的次数(tf)
        tfDict={}
        for docId in self.doc_ids:
            tfDict[docId] = {}
            for k in query:
               if k in self.index:
                   if docId in self.index[k]:
                       count = self.index[k][docId]
                   else:
                       count = 0
                   tfDict[docId][k] = count
        return tfDict
    
    # 计算含有query词的文件关于query词的idf
    def idfCalc(self,query,collectionSize):
        # df_w: number of documents containing w
        # 计算idf
        idfDict={}
        for k in query:
            if k in self.index:
                if len(self.index[k]) == 0:
                    idf = 0
                else:
                    idf = math.log(collectionSize / len(self.index[k]))
                idfDict[k] = idf
        return idfDict
    
    
    # 计算document中的tfidf值
    def tfIdfCalc(self,query,tfDict,idfDict):
        tfIdfDict = {}
        for docId in self.doc_ids:
            tfIdfDict[docId] = {}
            for k in query:
                if k in self.index:
                    tf = tfDict[docId][k]
                    idf = idfDict[k]
                    tfIdf = tf * idf
                    tfIdfDict[docId][k] = tfIdf
        return tfIdfDict
    
    # 计算query中的tfidf值
    def q_tfIdfCalc(self,query,idfDict):
        queryTfIdf = {}
        for k in query:
            if k in self.index:
                tf = query[k]
                idf = idfDict[k]
                tfIdf = tf * idf
                queryTfIdf[k] = tfIdf
        return  queryTfIdf    
        
        
        
    # 排序方法
    def rankTop(self,dict,size):
        top_10 = []
        sort = sorted(dict.items(),key=lambda x:-x[1])[:size]
        for docId,sim in sort:
            top_10.append(docId)
        return top_10
    
    
    # 处理queryList 返回set 排除重复词
    def processQuery(self,query):
        quertDict={}
        for q in query:
            if q in quertDict:
                quertDict[q] += 1
            else:
                quertDict[q] = 1
        return quertDict
