## General Guidelines

- reading and writing files should always implement encoding="utf-8"
- add informative print statements every step of the way to debug and see what the agent is doing and thinking
- have termcolor printing with cprint very step of the way to inform the user
- major variables should be all caps Variables on top of the script and not user input taking unless otherwise specified
- if there are models in the script like gpt-4o or gpt-4o-mini or o1-mini or o1-preview or claude-4-5-sonnet-20241022 do not change them as they now exist
- use pydantic
- do not delete requirements.txt unless you are sure it is not needed
- lets implement every project with seperation of concerns in mind
- always provide detailed instructions to the model considering everything carefully
- do not overcomplicate things. you should tend to simplify wherever possible
- do not mock codefiles if you suspect that they might already exist - rather, ask for the codefiles you need
- do not rewrite prompts or data classes unless specifically requested
- keep tests as simple executable and do not use mocks
- Always import python libraries at the top of the codefile
