from openai import OpenAI
import dotenv
import os
import asyncio

dotenv.load_dotenv()

class ChatOpenAI:
    def __init__(self, model_name: str, tools=[], system_prompt: str = "", context: str = ""):
        api_key = os.getenv("API_KEY")
        base_url = os.getenv("BASE_URL")  # 例如 https://api.deepseek.com
        self.model = model_name  # ✅ "deepseek-chat" 或 "deepseek-coder"
        self.tools = tools
        self.system_prompt = system_prompt
        self.context = context
        self.llm = OpenAI(api_key=api_key, base_url=base_url)
        self.message = []

    async def chat(self, prompt=None):
        if prompt:
            self.message.append({"role": "user", "content": prompt})

        params = {
            "model": self.model,
            "messages": self.message,
            "stream": True
        }
        tool_defs = self.getToolsDefinition()
        if tool_defs:
            params["tools"] = tool_defs

        stream = self.llm.chat.completions.create(**params)

        content = ""
        toolCalls = []

        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                contentChunk = delta.content or ""
                content += contentChunk
                print(contentChunk, end="", flush=True)
            if delta.tool_calls:
                for toolCallChunk in delta.tool_calls:
                    if len(toolCalls) <= toolCallChunk.index:
                        toolCalls.append({"id": "", "function": {"name": "", "arguments": ""}})
                    currentCall = toolCalls[toolCallChunk.index]
                    if toolCallChunk.id:
                        currentCall["id"] += toolCallChunk.id
                    if toolCallChunk.function.name:
                        currentCall["function"]["name"] += toolCallChunk.function.name
                    if toolCallChunk.function.arguments:
                        currentCall["function"]["arguments"] += toolCallChunk.function.arguments

        print()  # 输出换行
        self.message.append({
            "role": "assistant",
            "content": content,
            "tool_calls": [{"id": call["id"], "type": "function", "function": call["function"]} for call in toolCalls] if toolCalls else None
        })

        return {
            "content": content,
            "toolCalls": toolCalls
        }

    def appendToolResult(self, toolCallId: str, toolOutput: str):
        self.message.append({
            "role": "tool",
            "content": toolOutput,
            "tool_call_id": toolCallId
        })

    def getToolsDefinition(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": tool['name'],
                    "description": tool['description'],
                    "parameters": tool['inputSchema']
                }
            } for tool in self.tools
        ]


if __name__ == '__main__':
    async def main():
        prompt = "你是谁？"
        llm = ChatOpenAI("deepseek-chat")  # ✅ 注意不要写成 "deepseek/deepseek-chat"
        res = await llm.chat(prompt=prompt)
        print("\n最终结果:", res)

    asyncio.run(main())
