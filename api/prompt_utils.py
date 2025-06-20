from typing import List, Dict


def build_prompt(
        session_history: List[Dict[str, str]],
        new_prompt: str,
        system_instruction: str = "You are a helpful HR assistant who answers questions based on memory and internal HR policies."
) -> List[Dict[str, str]]:
    return [
        {"role": "system", "content": system_instruction},
        *session_history,
        {"role": "user", "content": new_prompt}
    ]
