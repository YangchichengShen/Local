from gemini import call_gemini_2_flash

example_news = '''
**AI Dominates Headlines:**

*   **OpenAI's GPT-4 Turbo Updates:** OpenAI continues to refine its flagship model, GPT-4 Turbo, with improvements in knowledge cutoff, accuracy, and context handling. There's also buzz around potential new features and capabilities being tested.
*   **AI Safety Concerns Persist:** Debates around AI safety and regulation are ongoing. Experts are discussing the potential risks of advanced AI systems and the need for responsible development and deployment.
*   **AI-Powered Tools Proliferate:** New AI-powered tools are emerging across various sectors, including marketing, content creation, and customer service. These tools promise increased efficiency and automation, but also raise questions about job displacement.

**Hardware and Devices:**

*   **Foldable Phone Competition Heats Up:** More manufacturers are entering the foldable phone market, challenging Samsung's dominance. Expect to see new designs and features aimed at improving durability and usability.
*   **VR/AR Advancements:** Companies are pushing forward with virtual and augmented reality technologies. There are reports of new headsets and software experiences in development, targeting both consumers and enterprise users.
*   **Chip Shortage Easing (But Not Gone):** The global chip shortage is showing signs of easing, but certain components remain in short supply. This is impacting production timelines and prices for various electronic devices.

**Big Tech and Business:**

*   **Layoffs Continue in Tech:** Despite some positive economic indicators, layoffs are still occurring at some major tech companies as they restructure and focus on profitability.
*   **Meta's Metaverse Push:** Meta continues to invest heavily in the metaverse, despite skepticism from some quarters. The company is working on new hardware and software experiences to attract users to its virtual world.
*   **Antitrust Scrutiny Intensifies:** Regulators around the world are increasing their scrutiny of Big Tech companies, focusing on issues such as market dominance, data privacy, and anti-competitive practices.

**Cybersecurity:**

*   **Ransomware Attacks Remain a Threat:** Ransomware attacks continue to be a major concern for businesses and organizations of all sizes. Security experts are urging companies to strengthen their defenses and implement robust backup and recovery plans.
*   **Data Breaches on the Rise:** Data breaches are becoming more frequent and sophisticated. Companies are facing increasing pressure to protect sensitive customer data and comply with data privacy regulations.

**Other Notable Developments:**

*   **Quantum Computing Progress:** Researchers are making steady progress in the field of quantum computing, with potential breakthroughs in areas such as drug discovery and materials science.
*   **Space Tech Advancements:** Space exploration and commercial space activities are gaining momentum. Companies are developing new rockets, satellites, and space-based services.

**Important Considerations:**

*   This is a rapidly evolving landscape, and new developments are constantly emerging.
*   The impact of these technologies on society, the economy, and the environment is a subject of ongoing debate.

'''

interests_json = {
  "interests": [
    "Patents",
    "Product Design",
    "Furniture Design (Desks, Chairs)",
    "Education (Courses, Lectures, Assignments)",
    "Job Search/Career Opportunities",
    "Fashion (Aritzia)",
    "Computer Science",
    "Security",
    "University Life (Northwestern)",
    "Online Collaboration Tools (Google Docs, Slides, Notion)",
    "Social Media (LinkedIn, Instagram)",
    "Research",
    "Internships"
  ]
}

contextify_prompt = '''
You are a news aggregator. Given the following interests, provide a contextified summary of the latest news that would be relevant to these interests. Respond with a JSON object where each key is an interest and the value is a brief news blurb related to that interest. The schema should be:

{
  "interest1": "news blurb for interest1",
  "interest2": "news blurb for interest2",
  ...
}
'''

# TODO: Change the interests_json and example_news to be dynamic based on user input or session state
def get_contextified_news(interests=interests_json, news=example_news):
    # Call the Gemini API to get the news contextified to the interests
    prompt = contextify_prompt + "\n\n" + str(interests) + "\n\n" + news
    result = call_gemini_2_flash(
        prompt = prompt,
        temperature=0.0
    )
    return result

# print(get_contextified_news(interests_json, example_news))
