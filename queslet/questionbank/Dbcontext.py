import pinecone

class connector():
    def __init__(self):
        pinecone.init(
            api_key='92425037-325f-4383-bc6e-f5a6da2a4caf',
            environment='us-east1-gcp'  # find next to API key in console
            )
# check if index already exists, if not we create it
        if 'qb-mcq-index' not in pinecone.list_indexes():
            pinecone.create_index(
            name='qb-mcq-index',
            dimension=768
            )
        self.index = pinecone.Index('qb-mcq-index')

    def query_mcqs_encode(self,encode,namespace,k=5,include_values=False,include_metadata=True):

        try:
            result = self.index.query(
        vector=encode,
        top_k=k,
        include_values=include_values,
        namespace=namespace,
        include_metadata=include_metadata
        )
        except:
            self.index = pinecone.Index('qb-mcq-index')
            result = self.index.query(
        vector=encode,
        top_k=k,
        include_values=include_values,
        namespace=namespace,
        include_metadata=include_metadata
        )


        return result



    # def query_mcqs_text(self,text,model,namespace,k=5,include_values=False,include_metadata=True):
    #     encode = model.encode(str(text)).tolist()
    #     return self.index.query(
    #     vector=encode,
    #     top_k=5,
    #     include_values=include_values,
    #     namespace=namespace,
    #     include_metadata=include_metadata
    #     )

# # connect to index
# index = pinecone.Index('qb-mcq-index')

# def query_mcqs(encode,namespace,k=5,include_values=False,include_metadata=True):
#     return index.query(
#     vector=encode,
#     top_k=5,
#     include_values=include_values
#     ,
#     namespace=namespace,
#     include_metadata=include_metadata
#     )