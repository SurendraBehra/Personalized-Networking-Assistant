# Project Demonstration - NetConnect

This document outlines the presentation slide structure, system demonstration scripts, and walkthrough video placeholders for NetConnect.

---

## 1. Walkthrough Demo Video Placeholder

A full walkthrough showing NetConnect's features has been recorded and is saved as a video artifact in our project records:
- **Recorded walkthrough name**: `netconnect_verification.webp` (created via autonomous E2E browser verification).
- **Video Placeholder**: `[Walkthrough Demonstration Video Link]` (to be uploaded to YouTube/Vimeo for public release).

---

## 2. Live Demonstration Script

Use the following step-by-step script to showcase NetConnect during live review calls or presentations:

### Setup Phase
1. Open a terminal and run `python run.py` inside `05_Project_Development/`.
2. Navigate to `http://localhost:8501` in your browser.
3. Open the sidebar and show that users can toggle between:
   - **Starter Generator**
   - **Quick Fact Verification**
   - **History & Feedback**

### Step 1: Starter Generation (AI Output vs. Fallback)
1. In the **Event Description** input field, type:
   `Web3 developers meet-up. Discussions on layer-2 rollup solutions, zk-STARKs, and decentralized validators.`
2. In the **Interests/Expertise** input field, type:
   `smart contract auditing, zero-knowledge scalability`
3. Leave the API key blank to show the **Fallback Template system** or enter a Gemini API Key to run the **Gemini generative pipeline**.
4. Click **Generate Starters**.
5. Show the UI rendering matching tags (e.g. `WEB3`, `SCALABILITY`, `SMART CONTRACTS`) and 3 beautiful open-ended conversational templates.

### Step 2: Reinforcement Loop
1. Click the green **Helpful** 👍 rating button on the first generated starter.
2. Note that the card updates immediately.

### Step 3: Quick Fact Verification
1. In the sidebar, select **Quick Fact Verification**.
2. Explain the use case: "If I'm talking to someone who mentions zk-STARKs and I want a fast summary, I search it here."
3. Type `zk-SNARK` in the search field and click **Search Wikipedia**.
4. Show the rendered information card with a concise paragraph summary and external link to Wikipedia.

### Step 4: History Logs Review
1. Select **History & Feedback** in the sidebar.
2. Show the log showing our Web3 meeting query.
3. Point out the "Thumbs Up" rating indicator, illustrating that this template will be injected as a few-shot instruction during the next generation cycle.

---

## 3. Presentation Slides Structure

For stakeholder presentations, we recommend organizing slides as follows:
1. **Title Slide**: NetConnect - Personalized Networking Assistant.
2. **The Problem**: Social friction, context gap, and knowledge recall panic at events.
3. **The Solution**: An intelligent assistant providing context-based few-shot starters and term lookup.
4. **Architecture**: Clean FastAPI + Streamlit layout with SQLite persistence.
5. **Key Tech Features**: Dynamic Few-Shot Prompting, Wiki search API, Offline Fallback Templates.
6. **Live Demo**: (Execute the live demonstration script above).
7. **Future Roadmap**: LinkedIn parsing, multi-model selection (GPT/Claude), mobile app support.
