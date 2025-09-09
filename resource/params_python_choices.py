def do(payload, config, plugin_config, inputs):
    import dataiku
    client = dataiku.api_client()
    tools_list = client.get_default_project().list_agent_tools()
   
    return {"choices": [
        {"label": tool["name"], "value": tool["id"]}
        for tool in tools_list
        if tool["type"] == "LLMMeshLLMQuery"
    ]}
    
    