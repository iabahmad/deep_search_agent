# Deep Search Agent

A multi-agent research and writing system powered by advanced language models and web search tools.

---

## Setup & Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/deep_search_agent.git
   cd deep_search_agent
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Create a `.env` file in the project root.
   - Add your API keys:
     ```
     DEEPSEEK_API_KEY=your_deepseek_api_key
     Gemini_API_KEY=your_gemini_api_key
     ```

4. **Run the system:**
   ```sh
   python main.py
   ```

---

## Example Research Questions

- "What are the latest advancements in quantum computing?"
- "Summarize the impact of AI on healthcare with sources."
- "Compare renewable energy policies in Europe and the US."
- "Write a professional report on climate change trends."

---

## Agent Roles

- **Helping Agent:**  
  Entry point. Plans tasks, asks for clarification, and delegates to the planner.

- **Planning Agent:**  
  Breaks down the query into sub-tasks, creates an execution plan, and delegates to the web search agent.

- **Web Search Agent:**  
  Performs web searches, gathers relevant information, checks sources, and passes results to the writer.

- **Professional Writer:**  
  Writes high-quality, comprehensive reports based on gathered information.

- **Premium Professional Writer:**  
  Adds source checking, conflict detection, synthesis, and citations for premium users.

---

## Team Coordination

Agents coordinate via a handoff system:
- Each agent delegates tasks it cannot complete to the next specialized agent.
- Handoffs are triggered based on task requirements and agent capabilities.
- Tools (like web search) are used when needed, and agents communicate results down the chain.
- The final output is synthesized and presented to the user.

---

##