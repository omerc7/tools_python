import inspect


from kubiya_sdk.tools.models import Tool, Arg, FileSpec
from kubiya_sdk.tools.registry import tool_registry

from . import main

hello_tool = Tool(
    name="get_weather",
    type="docker",
    image="python:3.12",
    description="Prints the weather",
    # args=[Arg(name="name", description="Name to greet", required=True)],
    content="""
pip install -r /tmp/requirements.txt

python /tmp/main.py
""",
    with_files=[
        FileSpec(
            destination="/tmp/requirements.txt",
            content="requests==2.32.3",
        ),
        FileSpec(
            destination="/tmp/main.py",
            content=inspect.getsource(main),
        ),
    ],
)

tool_registry.register("hello", hello_tool)
