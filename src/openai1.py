from openai import OpenAI
import os


text= "Speeding up image acquisition in MR- Magnetic resonance (MR) is another imaging modality that plays an ever-more important role in precision diagnosis of medical conditions. The rising use of MR is increasing the pressure to efficiently scan more patients and to shorten the path from initial scan to final diagnosis. At the same time, MR departments are looking for ways to improve satisfaction of patients and referring physicians."
prompt = f"Extract themes and summarize the main points from the following text:\n\n{text}\n\nSummarize as 3 keywords."


# OpenAI.api_key = "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" #os.environ["OPENAI_API_KEY"]
# client = OpenAI()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role":"developer", "content":"You are a qualitative data analyser who has studies linguistics. You can identify themes and subthemes in the given text and correlate them."},
        {"role": "user", "content": "Summarize this text and create 3 keywords: Speeding up image acquisition in MR- Magnetic resonance (MR) is another imaging modality that plays an ever-more important role in precision diagnosis of medical conditions. The rising use of MR is increasing the pressure to efficiently scan more patients and to shorten the path from initial scan to final diagnosis. At the same time, MR departments are looking for ways to improve satisfaction of patients and referring physicians." }
    ]
)

print(completion)