from MCPClient import MCPClient
from Agent import Agent
import os
from logTitle import logTitle
from EmbeddingRetriver import EmbeddingRetriver
os.environ["HTTP_PROXY"]="http://172.28.107.54:7890"
os.environ["HTTPS_PROXY"]="http://172.28.107.54:7890"
emb_model=os.getenv("EMBEDDING_MODEL")
current_dir=os.getcwd()
fetchMCP=MCPClient("fetch",command="uvx",args=['mcp-server-fetch'])
fileMCP=MCPClient("file",command="npx",args=['-y','@modelcontextprotocol/server-filesystem',current_dir])
print(f"current_dir is {current_dir}")
TASK=f"""告诉我 Chelsey Dietrich 的信息,先从我给你的文件中中找到相关信息,信息在 knowledge 目录下,总结后创作一个关于她的故事
        把故事和她的基本信息保存到{current_dir}/antonette.md,输出一个漂亮md文件"""
async def main():
    #简化流程，不再使用多层异常处理
    context=await retriveContext()
    
    logTitle("init Agent")
    agent=Agent("deepseek-chat",[fetchMCP,fileMCP],context=context)
    await agent.init()
    logTitle("init Agent finish")
    response=await agent.invoke(TASK)
    return response
async def retriveContext():
    #RAG
    embeddingRetriever=EmbeddingRetriver(model=emb_model)
    knowledgrDir=os.path.join(current_dir,"knowledge")
    for file in os.listdir(knowledgrDir):
        with open(os.path.join(knowledgrDir,file),'r',encoding='utf-8') as f:
            text=f.read()
            await embeddingRetriever.embedDocument(text)
    context=await embeddingRetriever.retrieve(TASK,3)
    logTitle(context)
    return context
if __name__=="__main__":
    import asyncio
    response=asyncio.run(main())
    print(response)
