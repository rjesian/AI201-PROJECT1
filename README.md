# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
This system covers unofficial student knowledge about life at Stony Brook University, sourced from the r/SBU subreddit. Topics include academic policies, course and professor recommendations, campus parking, dining hall quality, internship advice, and financial tips. This knowledge is valuable because it reflects real student experiences that never appear in official SBU handbooks, course catalogs, or university websites. A student wondering what actually happens when they fail a class, or which SBC courses are genuinely easy, cannot find a straight answer through official channels, but other students have already answered those questions in detail on Reddit.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 |r/SBU |Reddit thread |https://www.reddit.com/r/SBU/comments/1jzknv1/academic_dishonesty_advice_cs/ |
| 2 |r/SBU |Reddit thread |https://www.reddit.com/r/SBU/comments/1r1a2hj/aoi_in_cs/ |
| 3 |r/SBU |Reddit thread |https://www.reddit.com/r/SBU/comments/1c8ab9h/best_professors_in_physicsmath_departments_at_sbu/ |
| 4 |r/SBU |Reddit thread |https://www.reddit.com/r/SBU/comments/1tvblv7/bro_how_do_you_get_internships_am_i_cooked/ |
| 5 |r/SBU |Reddit thread |https://www.reddit.com/r/SBU/comments/1hkcg2x/hypothetically_i_failed_a_class/ |
| 6 |r/SBU |Reddit thread |https://www.reddit.com/r/SBU/comments/10dx2u6/parking_problem_on_campus/ |
| 7 |r/SBU |Reddit thread |https://www.reddit.com/r/SBU/comments/1tz4jz0/question_for_international_students_how_many_of/ |
| 8 |r/SBU |Reddit thread |https://www.reddit.com/r/SBU/comments/1rzcby8/small_tuition_life_hack/ |
| 9 |r/SBU |Reddit thread |https://www.reddit.com/r/SBU/comments/1gpkb64/what_are_easy_sbc_classes_to_take/ |
| 10 |r/SBU |Reddit thread |https://www.reddit.com/r/SBU/comments/1tchvkp/why_do_people_say_dining_hall_food_is_bad/ |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
500 characters

**Overlap:**
50 characters

**Why these choices fit your documents:**
My documents are Reddit threads made up of short student comments, most ranging from 2 to 6 sentences. A 500 character chunk is large enough to capture a complete thought or comment without pulling in unrelated content from a different part of the thread. A 50 character overlap ensures that if a useful idea falls across a chunk boundary, at least part of it appears in both chunks and stays retrievable. Before chunking, each document was cleaned to remove the Reddit URL at the bottom of each file and any empty lines. The TITLE, POST, and COMMENTS labels were kept because they provide useful context for the embedding model.


**Final chunk count:**
77 chunks across 10 documents

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
all-MiniLM-L6-v2 via sentence-transformers, running locally with no API key or rate limits.


**Production tradeoff reflection:**
For this project I used all-MiniLM-L6-v2 because it runs locally for free with no API key or rate limits. The main limitation is its 256 token context window, which means longer chunks can get cut off during embedding. If I were deploying this for real users I would look at OpenAI's text-embedding-3-small, which handles longer text better and produces more accurate results, though it costs money per request. I would also consider multilingual support since SBU has a large international student population and all-MiniLM-L6-v2 only works in English. For this project the local model was good enough, but a production system with real users would need something more capable.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->


**System prompt grounding instruction:**
The system prompt tells the model: "You are a helpful guide for Stony Brook University students. Answer the question using ONLY the information provided in the documents below. If the documents do not contain enough information to answer the question, say 'I don't have enough information on that topic.' Do not use any outside knowledge. Only use what is in the documents." This instruction is enforced every single time a question is asked, not just once at setup.



**How source attribution is surfaced in the response:**
After the LLM generates an answer, the system programmatically collects the source filenames from the retrieved chunks and displays them in a separate output box in the interface labeled "Retrieved from." This means source attribution is guaranteed by the pipeline itself, not left up to the LLM to include on its own.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What should I do if I am accused of academic dishonesty at SBU? | Appeal the case, show GitHub commits as evidence, guilty verdict requires unanimous vote from all 5 committee members | Correctly advised appealing, showing commits and diffs, explained the 5 member unanimous vote requirement | Relevant | Accurate |
| 2 | What are some easy SBC classes to take at SBU? | AMS 103, PHI 112, MUS 103, THR 101, SUS 200, ATM 103, PSY 103, POL 102 with specific professor recommendations | Returned correct class names but also listed SBC category codes like TECH, STAS, ARTS, DIV as if they were class names | Relevant | Partially accurate |
| 3 | What happens to my GPA if I fail a class and retake it at SBU? | Both grades show on transcript, averaged together for GPA, credits only count once | Correctly explained that both grades appear on transcript, are averaged, and credits only count once | Relevant | Accurate |
| 4 | How can commuter students park near the SAC at night for free? | Most permit lots free after 4pm, paid lots free after 7pm, South P bus runs until 11:30pm | Correctly identified free parking after 4pm behind ESS, at the plaza, and next to the stadium | Relevant | Accurate |
| 5 | What do students say about the quality of SBU dining hall food? | Mixed opinions, complaints about raw chicken and frozen food, some say it compares favorably to other schools | Accurately reflected mixed opinions including specific complaints about undercooked chicken and frozen food, and positive comparisons to other schools | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
What are some easy SBC classes to take at SBU?

**What the system returned:**
The system returned a mix of actual class names like AMS 103, PHI 112, and THR 101 alongside SBC category codes like TECH, STAS, ARTS, and DIV as if they were all class names. TECH, STAS, ARTS, and DIV are not classes, they are the SBC requirement categories those classes fulfill.

**Root cause (tied to a specific pipeline stage):**
This is a chunking issue. In the source document, the SBC codes appear directly next to class names without any explanation, for example "AMS 103 TECH PHI 112 STAS." When this text got chunked, the codes and class names ended up in the same chunk with no surrounding context to distinguish one from the other. The LLM read them as a flat list and treated everything as a class name.

**What you would change to fix it:**
I would go back to the source document and add a clarifying label before that line, for example "Class name followed by SBC category: AMS 103 (TECH), PHI 112 (STAS)." That additional context would survive chunking and give the LLM enough information to distinguish class names from category codes.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
Writing the chunking strategy in planning.md before touching any code forced me to actually think about the structure of my documents before deciding on chunk size. Because I had read through my Reddit threads before writing the spec, I knew most comments were short, which is why 500 characters made sense. If I had just picked a number randomly without the spec, I might have used something too large or too small and not understood why retrieval was failing.

**One way your implementation diverged from the spec, and why:**
In my planning.md I said I would remove the TITLE, POST, and COMMENTS labels from the documents during cleaning. During implementation I kept them because they actually provide useful context for the embedding model. A chunk that starts with "TITLE: Hypothetically I failed a class" gives the model more signal about what the document is about than a chunk that just starts mid-sentence. The spec was written before I fully understood how embeddings work, so this was a reasonable change to make once I had more context.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
My Chunking Strategy section from planning.md, which specified 500 character chunks with 50 character overlap, and my Documents section describing the .txt files in my redditdocs folder.
- *What it produced:*
An explanation of how chunking works with character boundaries and overlap, which I used to write the chunk_text() function with assisted coding.
- *What I changed or overrode:* 
I had to ask multiple follow up questions about how the overlap math worked before I understood it well enough to implement it. I also noticed on my own that the test code at the bottom of ingest.py was printing every time embed.py ran, diagnosed it as an import issue, and fixed it using the if __name__ == "__main__" guard after Claude explained what that does.

**Instance 2**

- *What I gave the AI:*
My Retrieval Approach section from planning.md and my pipeline diagram to establish context.
- *What it produced:*
An explanation of how ChromaDB stores and queries embeddings, which I used to write embed.py and retrieve.py.
- *What I changed or overrode:*
During retrieval testing I noticed a Reddit URL was still showing up in one of the results. I identified that the cleaning function was only catching lines that started with "LINK:" and missing URLs embedded elsewhere in the text. I added a check for any line containing "reddit.com", deleted the existing ChromaDB database, and rebuilt it with the fix applied.
