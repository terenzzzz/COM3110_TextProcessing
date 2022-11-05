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
        self.query = self.processQuery(query)
        self.candidate = self.getCandidate(self.query)
        
#==============================================================================       
        
        docVector={} # 包含特定模式数据的字典
        result = {} # 返回十个最相关文件的id
            
#==============================================================================
# Binary Mode
        if self.term_weighting == 'binary':
            # 判断query词是否出现在document中
            # 计算文件里有多少个Term
            doc_TermNum = self.compute_TermNum_doc()
            
            for doc in self.candidate:
                qd_product = 0
                d_vec_len = doc_TermNum[doc]
                
                for k in self.query:
                    if k in self.index:
                        if doc in self.index[k]:
                            count = 1
                        else:
                            count = 0
                        qd_product += count
                sim = qd_product / math.sqrt(d_vec_len)
                result[doc] = sim
            
#==============================================================================                    
# TF(Term Frequency) Mode

        elif self.term_weighting == 'tf':
            # 计算关键词出现在每篇文章中的次数
            docVector = self.tfCalc()
            
            doc_dPwd_sum = {}
            for term in self.index:
                for docId in self.index[term]:
                    if docId in doc_dPwd_sum:
                        doc_dPwd_sum[docId] += self.index[term][docId] * self.index[term][docId]
                    else:
                        doc_dPwd_sum[docId] = self.index[term][docId] * self.index[term][docId]
            
            # 调用相似度计算返回结果
            result = self.simCalc_tf(docVector, doc_dPwd_sum)
            
#==============================================================================    
# TF.IDF

        else:
            # 计算tf
            tfDict = self.tfCalc()

            # 计算tfIdf
            docVector = self.tfIdfCalc(tfDict)
            
            # 计算query中的tfidf值
            queryTfIdf = self.q_tfIdfCalc()
                        
            result = self.simCalc_tfIdf(queryTfIdf,docVector)
            
#==============================================================================
# Return 

        # 调用排序返回相似度最大的十个
        return self.rankTop(result,10)

#==============================================================================
# Calculation
    # 相似度计算(Binary)
    def simCalc_binary(self, doc_TermCount, docVector):
        result = {}
        for docId in docVector:
            pwdDSum = doc_TermCount[docId]
            qdSum = 0
            for term in docVector[docId]:
                q = 1
                d = docVector[docId][term]
                qdSum += q * d
            # 通过计算cos获取sim值
            cosVal = qdSum / math.sqrt(pwdDSum)
            result[docId] = cosVal
        return result
    
    # 相似度计算(TF)
    def simCalc_tf(self, docVector, doc_dPwd_sum):
        result = {}
        for docId in docVector:
            qdSum = 0
            dPwdSum = doc_dPwd_sum[docId]
            for term in docVector[docId]:
                q = self.query[term]
                d = docVector[docId][term]
                qdSum += q * d
            # 通过计算cos获取sim值
            cosVal = qdSum / math.sqrt(dPwdSum)
            result[docId] = cosVal
        return result
    
    def simCalc_tfIdf(self,queryTfIdf,docVector):
        result = {}
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
            if pwdDSum == 0:
                cosVal = 0
            else:
                cosVal = qdSum / math.sqrt(pwdDSum)
            result[docId] = cosVal
           
        return result
    
    
#==============================================================================
# Helper

    # 
    def compute_TermNum_doc(self):
        doc_TermNum = {}
        for term in self.index:
            for docId in self.index[term]:
                if docId in doc_TermNum:
                    doc_TermNum[docId] += 1
                else:
                    doc_TermNum[docId] = 0
        return doc_TermNum

    # 计算Term Frequency
    def tfCalc(self):
        # 计算关键词在每篇文章中出现的次数(tf)
        tfDict={}
        for docId in self.doc_ids:
            tfDict[docId] = {}
            for k in self.query:
                if k in self.index:
                    if docId in self.index[k]:
                        count = self.index[k][docId]
                    else:
                        count = 0
                    tfDict[docId][k] = count
                else:
                    tfDict[docId][k] = 0
        return tfDict
    
    # 计算document中的tfidf值
    def tfIdfCalc(self, tfDict):
        tfIdfDict = {}
        for docId in self.doc_ids:
            tfIdfDict[docId] = {}
            for k in self.query:
                if k in self.index:   
                    tf = tfDict[docId][k]
                    idf = math.log(self.num_docs / len(self.index[k]))
                    tfIdf = tf * idf
                    tfIdfDict[docId][k] = tfIdf
        return tfIdfDict
    
    # 计算query中的tfidf值
    def q_tfIdfCalc(self):
        queryTfIdf = {}
        for k in self.query:
            if k in self.index:
                tf = self.query[k]
                idf = math.log(self.num_docs / len(self.index[k]))
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
    
    # 获取候选文件id
    def getCandidate(self,query):
        candidateIdSet = set()
        for kw in query:
            if kw in self.index:
                for docId in self.index[kw]:
                    candidateIdSet.add(docId)
        return candidateIdSet