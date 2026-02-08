import inspect

from kubiya_sdk.tools.models import Tool, Arg, FileSpec
from kubiya_sdk.tools.registry import tool_registry

from . import main

dns_lookup_tool = Tool(
    name="dns_lookup",
    type="docker",
    image="python:3.12",
    description="Performs DNS lookup for a domain, returning A, AAAA, MX, NS, CNAME, and TXT records",
    args=[Arg(name="domain", description="Domain name to look up (e.g. example.com)", required=True)],
    content="""
curl -LsSf https://astral.sh/uv/0.4.30/install.sh | sh > /dev/null 2>&1
. $HOME/.cargo/env
uv venv > /dev/null 2>&1
. .venv/bin/activate > /dev/null 2>&1
uv pip install -r /tmp/requirements.txt > /dev/null 2>&1
python /tmp/main.py "{{ .domain }}"
""",
    with_files=[
        FileSpec(
            destination="/tmp/requirements.txt",
            content="dnspython==2.7.0\n",
        ),
        FileSpec(
            destination="/tmp/main.py",
            content=inspect.getsource(main),
        ),
    ],
)

tool_registry.register("dns_lookup", dns_lookup_tool)
