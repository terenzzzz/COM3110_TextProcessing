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
        self.result = {} # 返回十个最相关文件的id
        # 计算关键词出现在每篇文章中的次数
        self.doc_term_num = self.TermNum_doc()
            
#==============================================================================
# Binary Mode
        if self.term_weighting == 'binary':

            
            for doc in self.candidate:
                qd_product = 0
                d_vec_len = len(self.doc_term_num[doc])
                
                for k in self.query:
                    if k in self.index:
                        if doc in self.index[k]:
                            count = 1
                        else:
                            count = 0
                        qd_product += count
                sim = qd_product / math.sqrt(d_vec_len)
                self.result[doc] = sim
            
#==============================================================================                    
# TF(Term Frequency) Mode

        elif self.term_weighting == 'tf':
            for doc in self.candidate:
                qd_product = 0
                d_vec_len = 0
                
                # compute qd_product
                for term in self.query:
                    if term in self.index and doc in self.index[term]:
                        d = self.doc_term_num[doc][term]
                        q = self.query[term]
                        qd_product += d*q
                    
                # compute d_vec_len
                for term in self.doc_term_num[doc]:
                    d_vec_len += self.doc_term_num[doc][term] * self.doc_term_num[doc][term]

                sim = qd_product / math.sqrt(d_vec_len)
                self.result[doc] = sim
            
#==============================================================================    
# TF.IDF
        else:
            for doc in self.candidate:
                qd_product = 0
                d_vec_len = 0
                
                for term in self.query:
                    if term in self.index and doc in self.index[term]:
                        d_tf = self.doc_term_num[doc][term]
                        idf = math.log(self.num_docs / len(self.index[term]))
                        q_tf = self.query[term]
                        d_tfIdf = d_tf * idf
                        q_tfidf = q_tf * idf
                        qd_product += d_tfIdf * q_tfidf
                        
                for term in self.doc_term_num[doc]:
                    if term in self.index:
                        idf = math.log(self.num_docs / len(self.index[term]))
                        d = self.doc_term_num[doc][term] * idf
                        d_vec_len += d * d
                    
                      
                sim = qd_product / math.sqrt(d_vec_len)
                self.result[doc] = sim
#==============================================================================
# Return 
        # 调用排序返回相似度最大的十个
        return self.rankTop(self.result)

#==============================================================================
# Helper
    # 计算文章所有词出现次数
    def TermNum_doc(self):    
        doc_TermNum = {}
        for doc in self.candidate:
            doc_TermNum[doc] = {}
            
        for term in self.index:
            for doc in self.index[term]:
                num = self.index[term][doc]
                if doc in doc_TermNum:
                    if term not in doc_TermNum[doc]:
                        doc_TermNum[doc][term] = num
        return doc_TermNum
        
    # 排序方法
    def rankTop(self,result):
        top_10 = []
        sort = sorted(result.items(),key=lambda x:-x[1])[:10]
        for docId,sim in sort:
            top_10.append(docId)
        return top_10
    
    # 处理queryList 返回set 排除重复词
    def processQuery(self,query):
        quertDict={}
        for term in query:
            if term in quertDict:
                quertDict[term] += 1
            else:
                quertDict[term] = 1
        return quertDict
    
    # 获取候选文件id
    def getCandidate(self,query):
        candidateIdSet = set()
        for term in query:
            if term in self.index:
                for docId in self.index[term]:
                    candidateIdSet.add(docId)
        return candidateIdSet