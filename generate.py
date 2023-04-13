from llama import LLM, Context, Type
import json
import os

token = "cb01626747049cb05e1132c4f88b412c5ee8d169"
os.environ['LLAMA_ENVIRONMENT'] = "STAGING"
config = {
    "staging": {
        "key": token,
    }
}


llm = LLM(name="lamini-datasets", config=config)

# Get seed data, parse it
seed_tasks = [json.loads(l) for l in open("data/seed_tasks.jsonl", "r")]
seed_instruction_data = [
    {"instruction": t["instruction"], "input": t["instances"]
        [0]["input"], "output": t["instances"][0]["output"]}
    for t in seed_tasks
]
print(f"Loaded {len(seed_instruction_data)} human-written seed instructions")


# Generate more data like the seed data


class SeedData(Type):
    instruction: str = Context("An instruction that describes a task")
    input: str = Context("an input that provides further context")
    output: str = Context(
        "a response that appropriately completes the request")


seed_data = []
for datum in seed_instruction_data:
    seed_data.append(SeedData(instruction=datum['instruction'],
                     input=datum['input'],
                     output=datum['output'],))


class NewSeedData(Type):
    instruction: str = Context(
        "A new and diverse instruction that describes a task")
    input: str = Context("an new input that provides further context")
    output: str = Context(
        "a response that appropriately completes the request")


examples = seed_data[:3]
llm.add_data(examples)

seed_data = seed_data[3:]
generated_data = llm(input=seed_data, output_type=NewSeedData, random=True)

print("Generating new examples...")
print(generated_data)
