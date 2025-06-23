from typing import List, Dict

def build_prompt(
        session_history: List[Dict[str, str]],
        user_question: str,
        context: str = "",
        system_instruction: str = "You are a helpful HR assistant who answers questions based on memory and internal HR policies."
) -> List[Dict[str, str]]:
    messages = [{"role": "system", "content": system_instruction}]

    # Append memory
    messages.extend(session_history)

    # Prepend context with strong instructions if available
    if context:
        context_prompt = (
            "Use the following internal HR policy to answer the employee's question. "
            "If the answer requires reasoning (e.g., computing severance pay), explain your steps.\n\n"
            f"HR Policy:\n{context.strip()}"
        )
        messages.append({"role": "user", "content": context_prompt})

    # Final question
    messages.append({"role": "user", "content": user_question})
    print(user_question, "PROMPT")
    return messages
