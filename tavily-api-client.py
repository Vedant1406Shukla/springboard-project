from tavily import TavilyClient

tavily_client = TavilyClient(api_key="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")
response = tavily_client.search("Who is Leo Messi?")

print(response)