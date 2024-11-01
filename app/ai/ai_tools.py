import os

import google.generativeai as genai


api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel(safety_settings="BLOCK_NONE")


def moderate_text(text):
    prompt = (f"You are a moderator, "
              f"Check the following text for obscene words, hate speech, insults, or any other inappropriate content."
              f"Note that only dangerous content should be banned, some rude words can be allowed in artistic style or to enhance the emotion."
              f"Text can be written on any language."
              f"Give your verdict and response 'OK' if the text is appropriate, or 'BAN' if it should be banned."
              f"\n\n\n{text}")

    response = model.generate_content(prompt)
    return response.text


def reply_comment(post, comment):
    prompt = (f"Give a relevant reply to the following comment:\n***{comment}***"
              f"\nThe comment was made on the post:\n***{post}***"
              f"Reply should be polite and respectful, and should not contain any inappropriate content."
              f"Reply on language that comment was written in")

    response = model.generate_content(prompt)
    return response.text

