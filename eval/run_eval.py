from pipeline import run_copilot
from pathlib import Path
import re

def load_prompts(file_path: str):
    text = Path(file_path).read_text(encoding="utf-8")
    lines = [re.sub(r"^\d+\.\s*", "", line).strip() for line in text.splitlines()]
    prompts = [line for line in lines if line]

    return prompts


def run_evaluation():
    prompts = load_prompts("eval/test_prompts.txt")

    passes = 0
    fails = 0
    total_tokens_all = 0

    for i, prompt in enumerate(prompts, 1):
        print(f"\n=== Test {i} ===")
        print("Prompt:", prompt)

        result = run_copilot(prompt)

        verification = result.get("verification", "UNKNOWN")

        if verification.startswith("PASS"):
            passes += 1
        else:
            fails += 1

        total_tokens = sum(
            step.get("total_tokens", 0)
            for step in result.get("trace", [])
        )

        total_tokens_all += total_tokens

        print("Verification:", verification)
        print("Total Tokens:", total_tokens)

    # ✅ ADD THIS SUMMARY SECTION
    print("\n===== EVALUATION SUMMARY =====")
    print("Total Tests:", len(prompts))
    print("Pass:", passes)
    print("Fail:", fails)
    print("Total Tokens Used:", total_tokens_all)


if __name__ == "__main__":
    run_evaluation()
