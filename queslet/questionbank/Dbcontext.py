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
# row = (qid,encode,{'question':question,'answer':str(answer_q),'contain_images':contain,'image':q_image})

    def upload(self,qid,encode,question,contain,q_image,subject):
        # print(type(encode))
        # print(encode)
        # print("Upload ID",qid)

        row =[ (qid,list(encode),{'question':str(question),'contain_images':contain,'image':str(q_image)})]

        # print(row)

        try:
            result = self.index.upsert(row,namespace=subject)
        except:
            self.index = pinecone.Index('qb-mcq-index')
            result = self.index.upsert(row,namespace=subject)
        return result

