# Do we need to process the query
# Index mean in engine
# Query mean in engine
# The return in for_query
# Goal: Find The Best 10 Document  for each queries?
# What method to rank (queries has many words) term_weighting???




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


        
        return list(range(1,11))

    # articles
    def query(self,keyword):
        print(1)
        