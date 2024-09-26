from kubiya_sdk.tools.models import Tool, Arg
from kubiya_sdk.tools.registry import tool_registry

hello_tool = Tool(
    name="hello",
    type="docker",
    image="python:3.11",
    description="Prints hello world",
    args=[Arg(name="name", description="Name to greet", required=True)],
    content="python -c \"print(f'Hello {name}')\"",
)


tool_registry.register("hello", hello_tool)
