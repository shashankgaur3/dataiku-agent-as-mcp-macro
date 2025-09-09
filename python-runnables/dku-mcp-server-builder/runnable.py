# This file is the actual code for the Python runnable dku-mcp-server-builder
from dataiku.runnables import Runnable
import dataiku
import os

SERVER_PYTHON_FILE='''
import dataiku
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="{name}", 
        instructions="{instructions}",
        host="0.0.0.0", port="{port}"
    )
{tools}

if __name__ == "__main__":
    mcp.run(transport='streamable-http')

'''

TOOL_FUNCTIONS='''
@mcp.tool()
async def {name}(query: str) -> str:
    """
    {description}
    
    Args:
        query: User query
    
    Returns:
        Generated response as string.
    """
    
    client = dataiku.api_client()
    tool = client.get_default_project().get_agent_tool("{tool_id}")
    output = tool.run({{"question": query}})
    return output['output']['response']
    
'''

class MyRunnable(Runnable):
    """The base interface for a Python runnable"""

    def __init__(self, project_key, config, plugin_config):
        """
        :param project_key: the project in which the runnable executes
        :param config: the dict of the configuration of the object
        :param plugin_config: contains the plugin settings
        """
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config
        
    def get_progress_target(self):
        """
        If the runnable will return some progress info, have this function return a tuple of 
        (target, unit) where unit is one of: SIZE, FILES, RECORDS, NONE
        """
        return None

    def run(self, progress_callback):
        """
        Do stuff here. Can return a string or raise an exception.
        The progress_callback is a function expecting 1 value: current progress
        """
        # Get Input Params
        mcp_name = self.config.get("name").strip()
        mcp_instructions = self.config.get("instructions","")
        mcp_port = self.config.get("port")
        mcp_tools = self.config.get("agentTools")
        
        # Validate required inputs
        if mcp_name is None:
            raise Exception("MCP Name can not be null")
        if not mcp_tools:
            raise Exception("Atleast one Tool should be selected")
        
        # Get the project object
        project_obj = dataiku.api_client().get_default_project()
        lib_obj = project_obj.get_library()
        
        # Get the Library Python/mcp folder. If mcp folder doesn't exist, create it.
        python_folder = lib_obj.get_folder("python")
        mcp_folder = python_folder.get_folder("mcp")
        if mcp_folder is None:
            mcp_folder = python_folder.add_folder("mcp")
            
        # Create the mcp server file using name variable
        mcp_name_formatted = mcp_name.replace(" ", "_").lower()
        file_ext=".py"
        version = 1
        filename = mcp_name_formatted + file_ext
        
        # This loop checks if the file already exist, if yes it appends a incremented version to it like v1, v2 ..
        while mcp_folder.get_file(filename) is not None:
            filename = f"{mcp_name_formatted}_v{version}{file_ext}"
            version += 1
        
        mcp_server_file=mcp_folder.add_file(filename)
        
        # For every tool added as the input, it will generate a mcp tool function
        tool_functions = ""
        for tool in mcp_tools:
            tool_metadata = project_obj.get_agent_tool(tool).get_descriptor()
            tool_name = tool_metadata["name"].rsplit('_',1)[0].lower()
            tool_desc = tool_metadata["description"]
            
            # Get tool Purpose + Additional Description as MCP Tool Description
            tool_desc = tool_desc[tool_desc.find(".")+1:]
            tool_functions += TOOL_FUNCTIONS.format(name=tool_name, description=tool_desc, tool_id=tool)
            
        # Writes the final python file in the projects library
        data_file=SERVER_PYTHON_FILE.format(name=mcp_name, instructions=mcp_instructions, port=mcp_port, tools=tool_functions)
        mcp_server_file.write(data_file)
        
        # Returns the file name in the macro output
        return "MCP Server File has been successfully created in Project Libraries: " + filename
        
        