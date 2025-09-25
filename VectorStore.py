class VectorItem:
    def __init__(self,embedding,text):
        self.embedding = embedding
        self.text = text
class VectorStore:
    def __init__(self):
        self.vectorStore:list[VectorItem]=[]
    def addEmbedding(self,embedding,text):
        self.vectorStore.append(VectorItem(embedding,text))
    def search(self,query,topk:int=3):
        score_list=sorted(self.vectorStore,key=lambda x:self.cosSim(query,x.embedding),reverse=True)
        return [item.text for item in score_list[:topk]]
    def cosSim(self,vec1,vec2):
        dot_product=sum(a*b for a,b in zip(vec1,vec2))
        norm_a=sum(a*a for a in vec1)
        norm_b=sum(b*b for b in vec2)
        if norm_a==0 or norm_b==0:return 0
        return dot_product/(norm_a*norm_b)
