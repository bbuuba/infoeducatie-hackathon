from openai import OpenAI
client = OpenAI()

# Define the personalities
personalities = {
    'AI1': 'Friendly and supportive, always encouraging.',
    'AI2': 'Competitive and strategic, focused on winning.',
    'AI3': 'Curious and inquisitive, asking questions.',
    'AI4': 'Analytical and logical, making reasoned decisions.',
    'AI5': 'Creative and imaginative, thinking outside the box.'
}

# Initialize conversation histories for each AI
conversation_histories = {ai_id: [] for ai_id in personalities}

def generate_prompt(personality, history, current_prompt):
    # Build the prompt incorporating personality and historical context
    prompt = f"Personality: {personality}\n"
    prompt += "Conversation History:\n" + "\n".join(history) + "\n"
    prompt += "Current Prompt:\n" + current_prompt + "\n"
    return prompt

def ai_function(ai_id, current_prompt):
    # Get personality and conversation history for the specified AI
    personality = personalities[ai_id]
    conversation_history = conversation_histories[ai_id]
    
    # Generate the full prompt including personality and history
    prompt = generate_prompt(personality, conversation_history, current_prompt)

    # Request completion from OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You are an AI with the following personality: {personality}."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the AI's response
    direction = response.choices[0].message

    # Update the conversation history
    conversation_history.append(f"User: {current_prompt}")
    conversation_history.append(f"AI: {direction}")

    # Save updated conversation history
    conversation_histories[ai_id] = conversation_history

    return direction

# Example usage
#if __name__ == "__main__":
    # Query each AI with the same prompt
    prompt = 'What is your plan for the game?'
    
 #   for ai_id in personalities:
  #      response = ai_function(ai_id, prompt)
   #     print(f"{ai_id}: {response}")
