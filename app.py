import os
from groq import Groq
from dotenv import load_dotenv
from retrieve import retrieve
import gradio as gr

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask(question):
    chunks = retrieve(question)

    context = ""
    sources = []
    for chunk in chunks:
        context += chunk["text"] + "\n\n"
        if chunk["source"] not in sources:
            sources.append(chunk["source"])
    prompt = f"""You are a helpful guide for Stony Brook University students.
    Answer the question using ONLY the information provided in the documents below.
    If the documents do not contain enough information to answer the question, say
    "I don't have enough information on that topic." Do not use any outside 
    knowledge. Only use what is in the documents.
    
    Documents: {context}

    Question: {question}
    
    Answer: """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content

    return {"answer": answer, "sources": sources}

def handle_query(question):
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources

with gr.Blocks() as demo:
    inp = gr.Textbox(label="Your question")
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()

    

    