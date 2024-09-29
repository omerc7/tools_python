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
curl -LsSf https://astral.sh/uv/install.sh | sh > /dev/null 2>&1
. $HOME/.cargo/env

uv venv > /dev/null 2>&1
. .venv/bin/activate > /dev/null 2>&1

uv pip install -r /tmp/requirements.txt > /dev/null 2>&1

python /tmp/main.py
""",
    with_files=[
        FileSpec(
            destination="/tmp/requirements.txt",
            content="""
requests==2.32.3
pydantic==2.9.2
""",
        ),
        FileSpec(
            destination="/tmp/main.py",
            content=inspect.getsource(main),
        ),
    ],
)

tool_registry.register("hello", hello_tool)
