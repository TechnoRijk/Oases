# gpt_operations.py

from flask import jsonify
import openai

def rewrite_post_with_gpt(post_content):
    try:
        prompt = f"Rewrite the following post: {post_content}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except openai.Error as e:
        return f"Failed to rewrite post: {str(e)}"
