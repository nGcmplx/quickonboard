from typing import List, Dict

def build_prompt(
        session_history: List[Dict[str, str]],
        user_question: str,
        context: str = "",
        system_instruction: str = "You are a helpful HR assistant who answers questions strictly based on internal HR policies."
) -> List[Dict[str, str]]:
    messages = [{"role": "system", "content": system_instruction}]

    # Append memory
    messages.extend(session_history)

    # Inject full context with strong guardrails
    if context:
        context_prompt = (
            "Answer the following question using only the HR policy below. "
            "Do not guess or make things up. If the answer is not clearly in the policy, respond with 'I don't know.'\n\n"
            f"HR Policy:\n{context.strip()}"
        )
        messages.append({"role": "user", "content": context_prompt})

    # Final user prompt
    messages.append({"role": "user", "content": user_question})

    return messages
