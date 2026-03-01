import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    args = parser.parse_args()

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = None
    for _ in range(20):
        response, messages = generate_content(client, messages, args)
        if response:
            break
    
    if response:
        print('Final response:')
        print(response.text)
    else:
        print('Could not get a response')

def generate_content(client, messages, args):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    if args.verbose:
        print_response_metadata(response, args.user_prompt)

    if response.candidates:
        for c in response.candidates:
            if c.content:
                messages.append(c.content)

    # Print client response to console
    if response.function_calls:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, args.verbose)

            if (
                function_call_result.parts is None
                or not function_call_result.parts
                or function_call_result.parts[0].function_response is None
                or function_call_result.parts[0].function_response.response is None
            ):
                raise Exception(
                    f"Something went wrong during the {function_call.name} function call, with args {function_call.args}"
                )
            function_results = [function_call_result.parts[0]]
            messages.append(types.Content(role="user", parts=function_results))
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
        return None, messages
    else:
        messages.append([types.Content(role="model", parts=[types.Part(text=response.text)])])
        return response, messages



def print_response_metadata(response, user_prompt):
    usage_metadata = response.usage_metadata
    if usage_metadata is None:
        raise RuntimeError("could not read api client response, something went wrong")
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
    print(f"Response tokens: {usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
