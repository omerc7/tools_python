from kubiya_sdk.tools.models import Tool, Arg, FileSpec
from kubiya_sdk.tools.registry import tool_registry

hello_tool = Tool(
    name="hello",
    type="docker",
    image="python:3.11",
    description="Prints hello world",
    # args=[Arg(name="name", description="Name to greet", required=True)],
    content="python /tmp/bla.py",
    with_files=[
        FileSpec(
            destination="/tmp/bla.py",
            content="print('Hello from file')",
        )
    ],
)

tool_registry.register("hello", hello_tool)
