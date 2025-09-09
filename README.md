# Dataiku Agent as MCP Macro

This Dataiku plugin provides a Macro that generates a Python server file for the Model Context Protocol (MCP) framework. The generated server exposes selected Dataiku Agent Tools from your project as callable tools for an LLM.

## Overview

It provides a user-friendly Macro that:
1.  Scans your project for available Agent Tools.
2.  Lets you select which ones to publish.
3.  Generates a standalone `FastMCP` Python server script.

This script can be setup as a server using Dataiku Code Studios that an MCP client (like Claude Desktop) can connect to and use the exposed Agent Tools.

## Features

-   **Simple Interface**: A straightforward macro to configure and generate your MCP server.
-   **Dynamic Tool Discovery**: Automatically lists `LLMMeshLLMQuery` type Agent Tools from the current project.
-   **Custom Configuration**: Set a custom name, instructions, and port for your MCP server.
-   **Code Generation**: Creates a clean, ready-to-run Python script.
-   **Project Library Integration**: Saves the generated script directly into your project's library (`python/mcp/`) for easy management and versioning.
-   **Automatic Versioning**: Avoids overwriting existing files by appending a version number (e.g., `my_server_v1.py`) if a file with the same name already exists.

## How to Use

### Prerequisites

1.  A running Dataiku instance.
2.  This plugin installed on the instance.
3.  A Dataiku project where you have created one or more Agent Tools. The macro will specifically look for tools of type `LLMMeshLLMQuery`.

### Steps

1.  Navigate to your Dataiku project.
2.  From the top navigation bar, click on **Macros**.
3.  Select the **Dataiku Agents as MCP Tools** macro.
4.  A dialog box will appear with the following parameters:
    -   **Select Agent Tools**: A multi-select dropdown listing all compatible Agent Tools in your project. Choose one or more.
    -   **MCP Server Name**: A descriptive name for your server (e.g., "Project Finance Tools").
    -   **MCP Server Instructions**: (Optional) Instructions for the LLM on what the tools are for and how to use them effectively.
    -   **Server Port**: The network port the server will listen on. Defaults to `40000`.
5.  Click **Run Macro**.

## Output

Upon successful execution, the macro will create a new Python file in your project's library. You can find it in:

`Project > Library > python > mcp > <your_server_name>.py`

The macro will return a success message indicating the name of the file created.

## Next Steps

The macro only *generates* the server script; it does not run it.

To setup the server, you can follow this tutorial (https://developer.dataiku.com/latest/tutorials/genai/agents-and-tools/mcp/my-mcp/index.html) from Dataiku Developer Guide.
