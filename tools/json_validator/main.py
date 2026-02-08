import argparse
import json
import sys

from jsonschema import validate, ValidationError, SchemaError


def validate_json(json_string, schema_string=None):
    # Parse the JSON input
    try:
        data = json.loads(json_string)
    except json.JSONDecodeError as e:
        print("JSON Validation Result: INVALID")
        print("=" * 40)
        print(f"  Parse Error: {e.msg}")
        print(f"  Line: {e.lineno}, Column: {e.colno}")
        return

    print("JSON Validation Result: VALID SYNTAX")
    print("=" * 40)
    print(f"  Type:     {type(data).__name__}")
    if isinstance(data, (list, dict)):
        print(f"  Length:   {len(data)}")

    # Schema validation if provided
    if schema_string:
        try:
            schema = json.loads(schema_string)
        except json.JSONDecodeError as e:
            print(f"\n  Schema Parse Error: {e.msg}")
            return

        try:
            validate(instance=data, schema=schema)
            print(f"\n  Schema Validation: PASS")
        except SchemaError as e:
            print(f"\n  Schema Error: Invalid schema")
            print(f"    {e.message}")
        except ValidationError as e:
            print(f"\n  Schema Validation: FAIL")
            print(f"    Error:   {e.message}")
            if e.absolute_path:
                path = ".".join(str(p) for p in e.absolute_path)
                print(f"    Path:    {path}")
            print(f"    Rule:    {e.validator} = {e.validator_value}")

    # Pretty-print the parsed JSON
    print("\nParsed JSON:")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate a JSON string")
    parser.add_argument("json_string", help="JSON string to validate")
    parser.add_argument("--schema", default=None, help="Optional JSON Schema to validate against")
    args = parser.parse_args()
    validate_json(args.json_string, args.schema)
