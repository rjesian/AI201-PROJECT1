# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
I chose the Stony Brook University subreddit (r/SBU). it contains unofficial student knowledge about life at SBU. things like how grading and retakes work, parking tips for commuters, easy A classes, dining hall quality, internship advice, and academic dishonesty processes. Stuff that exists in student convos but not in any official SBU handbook

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 |r/SBU |Student asking for advice on fighting an academic dishonesty accusation in a CS class |https://www.reddit.com/r/SBU/comments/1jzknv1academic_dishonesty_advice_cs/ |
| 2 |r/SBU |Freshman AOI student in CS asking about getting into the major and double majoring |https://www.reddit.com/r/SBU/comments/1r1a2hj/aoi_in_cs/ |
| 3 |r/SBU |Students sharing best and worst physics and math professors at SBU |https://www.reddit.com/r/SBU/comments/1c8ab9h/best_professors_in_physicsmath_departments_at_sbu/ |
| 4 |r/SBU |Students discussing how to get internships and the importance of networking |https://www.reddit.com/r/SBU/comments/1tvblv7/bro_how_do_you_get_internships_am_i_cooked/ |
| 5 |r/SBU |Student asking what happens if they fail a class and how retaking affects GPA |https://www.reddit.com/r/SBU/comments/1hkcg2x/hypothetically_i_failed_a_class/ |
| 6 |r/SBU |Commuter student asking about parking options near SAC at night |https://www.reddit.com/r/SBU/comments/10dx2u6/parking_problem_on_campus/ |
| 7 |r/SBU |International students discussing job prospects after graduating from SBU |https://www.reddit.com/r/SBU/comments/1tz4jz0/question_for_international_students_how_many_of/ |
| 8 |r/SBU |Students sharing a tuition life hack using credit cards to earn points |https://www.reddit.com/r/SBU/comments/1rzcby8/small_tuition_life_hack/ |
| 9 |r/SBU |Students recommending easy SBC classes and which professors to take them with |https://www.reddit.com/r/SBU/comments/1gpkb64/what_are_easy_sbc_classes_to_take/ |
| 10|r/SBU |Students debating whether SBU dining hall food is actually bad |https://www.reddit.com/r/SBU/comments/1tchvkp/why_do_people_say_dining_hall_food_is_bad/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
500 characters

**Overlap:**
50 characters

**Reasoning:**
My documents are Reddit threads made up of short student comments, most ranging from 2 to 6 sentences. A 500 character chunk is large enough to capture a complete thought or comment without pulling in unrelated content from a different part of the thread. A 50 character overlap ensures that if a useful idea falls across a chunk boundary, at least part of it appears in both chunks and stays retrievable.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
all-MiniLM-L6-v2 via sentence-transformers


**Top-k:**
5

**Production tradeoff reflection:**
 For a real deployment I would consider a few tradeoffs. all-MiniLM-L6-v2 is fast and free but it has a short context window of 256 tokens, which could cause it to truncate longer chunks. A model like text-embedding-3-small from OpenAI would handle longer text better and likely be more accurate, but costs money per request. If SBU had international students using the system in other languages, multilingual support would also matter — all-MiniLM-L6-v2 is English-only. For a student-facing tool at this scale, the local free model is fine, but a production system would likely justify paying for a better one.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 |What should I do if I am accused of academic dishonesty at SBU?  | Students recommend appealing the case, showing GitHub commits as evidence, and noting that the Academic Judiciary Committee requires a unanimous vote of all 5 members for a guilty verdict.  |
| 2 | What are some easy SBC classes to take at SBU?  | Students recommend AMS 103 for TECH, PHI 112 for STAS, MUS 103 for ARTS, THR 101, SUS 200, ATM 103 for STAS, PSY 103 for CER, and POL 102 for USA.  |
| 3 | What happens to my GPA if I fail a class and retake it at SBU?  | Both grades show on the transcript and are averaged together for GPA. Credits only count once. An F averaged with an A results in approximately a C.  |
| 4 | How can commuter students park near the SAC at night for free?  | Most permit lots are free after 4pm and most paid/metered lots are free after 7pm. Students can also park in South P and take the bus which runs until around 11:30pm. The Outer Loop also stops at the LIRR station at 11:30pm.  |
| 5 | What do students say about the quality of SBU dining hall food?  | Opinions are mixed. Some students enjoy it especially ESD and WSD. Common complaints include raw chicken, reheated frozen food, and high cost per swipe. Some feel it compares favorably to other schools.  |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. My documents are Reddit threads which contain jokes, one-word replies, slang, and off-topic comments mixed in with  useful information. When these get chunked, a chunk might contain nothing but a joke or a useless one-liner. That chunk could still get retrieved and confuse the AI into generating a bad or irrelevant answer.

2. Some of the most useful comments in my documents are long and span multiple sentences that build on each other. If a chunk cuts that comment in half, neither chunk tells the full story on its own.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

```
Document Ingestion        Chunking                 Embedding + Vector Store        Retrieval                Generation
--------------------      --------------------     ------------------------        --------------------     --------------------
.txt files loaded    -->  Split into 500 char  --> all-MiniLM-L6-v2 embeds   --> Semantic search in  --> Groq API
from documents/          chunks with 50 char      each chunk, stored in           ChromaDB returns         llama-3.3-70b
folder using             overlap using            ChromaDB with source            top 5 relevant           generates answer
Python open()            Python string            filename metadata               chunks for query         from retrieved
                         splitting                                                                         chunks only
```

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

     

**Milestone 3 — Ingestion and chunking:**
I will use Claude as a guide. I will share my Documents section and Chunking Strategy section and ask it to explain how to write a script that loads .txt files and splits them into 500 character chunks with 50 character overlap. I will write the code myself with Claude helping me understand any parts I get stuck on. I will verify by printing 5 random chunks and checking they are readable and complete.

**Milestone 4 — Embedding and retrieval:**
I will use Claude when I get stuck on ChromaDB setup and the retrieval function since those are new concepts to me. I will share my Retrieval Approach section and Architecture diagram for context. I will verify by running 3 of my evaluation questions and checking that the returned chunks relate to each question.

**Milestone 5 — Generation and interface:**
I will use Claude to help me understand how to connect the Groq API to my retrieval function and how to set up a basic Gradio interface. I will share my grounding requirement and output format so Claude understands what I need. I will verify by testing an out-of-scope question and confirming the system declines to answer instead of making something up.
