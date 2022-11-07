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
        
        self.doc_term_num() # pre-compute the number of term in every document
        
        if self.term_weighting == 'tfidf':
            self.idf_doc_term() 
        
        # pre-compute the document vector length in every document
        if self.term_weighting != 'binary':
            self.doc_vec_len_dict = {}
            for doc in self.doc_term_num:
                self.doc_vec_len_dict[doc] = 0
                for term in self.doc_term_num[doc]:
                    if self.term_weighting == 'tf':
                        self.doc_vec_len_dict[doc] += self.doc_term_num[doc][term] * self.doc_term_num[doc][term]
                    elif self.term_weighting == 'tfidf':
                        idf = self.idfDict[doc][term]
                        d = self.doc_term_num[doc][term] * idf
                        self.doc_vec_len_dict[doc] += d * d


    def compute_number_of_documents(self):
        self.doc_ids = set() 
        for term in self.index:
            self.doc_ids.update(self.index[term])
        return len(self.doc_ids)
    

    # Method performing retrieval for a single query (which is 
    # represented as a list of preprocessed terms). Returns list 
    # of doc ids for relevant docs (in rank order).
    def for_query(self, query):
        # pre-process the query into a dictionary to advoide same terms
        self.query = self.processQuery(query)
        # return self.candidate about all the document related to the query
        self.getCandidate(self.query) 
        # to save top 10 relevent document id
        self.result = {} 
        
#==============================================================================
# Binary Mode
        if self.term_weighting == 'binary':
            # loop to calculate similarity for all the candidate document
            for doc in self.candidate:
                qd_product = 0
                # the size of the document
                d_vec_len = len(self.doc_term_num[doc])
                
                # Calculate the qd_product for this document
                for k in self.query:
                    if k in self.index:
                        if doc in self.index[k]:
                            count = 1
                        else:
                            count = 0
                        qd_product += count
                        
                # similarity calculation
                sim = qd_product / math.sqrt(d_vec_len)
                self.result[doc] = sim
            
#==============================================================================                    
# TF(Term Frequency) Mode

        elif self.term_weighting == 'tf':
            # loop to calculate similarity for all the candidate document
            for doc in self.candidate:
                qd_product = 0
                d_vec_len = self.doc_vec_len_dict[doc]
                
                # Calculate the qd_product for this document
                for term in self.query:
                    if term in self.index and doc in self.index[term]:
                        d = self.doc_term_num[doc][term]
                        q = self.query[term]
                        qd_product += d*q
                    
                # similarity calculation
                sim = qd_product / math.sqrt(d_vec_len)
                self.result[doc] = sim
            
#==============================================================================    
# TF.IDF
        else:
            # loop to calculate similarity for all the candidate document
            for doc in self.candidate:
                qd_product = 0
                d_vec_len = self.doc_vec_len_dict[doc]
                
                # Calculate the qd_product for this document
                for term in self.query:
                    if term in self.index and doc in self.index[term]:
                        idf = self.idfDict[doc][term]
                        d_tf = self.doc_term_num[doc][term]
                        q_tf = self.query[term]
                        d_tfIdf = d_tf * idf
                        q_tfidf = q_tf * idf
                        qd_product += d_tfIdf * q_tfidf
                    
                # similarity calculation    
                sim = qd_product / math.sqrt(d_vec_len)
                self.result[doc] = sim
#==============================================================================
# Return 
        # 调用排序返回相似度最大的十个
        return self.rankTop(self.result)

#==============================================================================
# Helper

    # Compute the number of terms appear in every document
    def doc_term_num(self):    
        self.doc_term_num = {}
        for doc in self.doc_ids:
            self.doc_term_num[doc] = {}
        for term in self.index:
            for doc in self.index[term]:
                num = self.index[term][doc]
                if doc in self.doc_term_num :
                    if term not in self.doc_term_num [doc]:
                        self.doc_term_num[doc][term] = num
    
    # Idf for the terms in every document
    def idf_doc_term(self):
        self.idfDict = {}
        for doc in self.doc_term_num:
            self.idfDict[doc] = {}
            for term in self.doc_term_num[doc]:
                self.idfDict[doc][term]= math.log(self.num_docs / len(self.index[term]))
                

    
    # Rank the top 10 document and return a list of id
    def rankTop(self,result):
        top_10 = []
        sort = sorted(result.items(),key=lambda x:-x[1])[:10]
        for docId,sim in sort:
            top_10.append(docId)
        return top_10
    
    # Pre-process the query to advoide same terms
    def processQuery(self,query):
        quertDict={}
        for term in query:
            if term in quertDict:
                quertDict[term] += 1
            else:
                quertDict[term] = 1
        return quertDict
    
    # Get candidate document and return a set of docId
    def getCandidate(self,query):
        self.candidate = set()
        for term in query:
            if term in self.index:
                for docId in self.index[term]:
                    self.candidate.add(docId)