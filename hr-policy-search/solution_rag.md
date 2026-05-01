# ShopEase AI Support Assistant: Transitioning to RAG

## Q1. Why did the plain ChatGPT-style chatbot give wrong answers?

The plain ChatGPT-style chatbot failed because it lacked access to ShopEase’s internal, domain-specific data. Rooted in its general training data, the model's knowledge is static and cut off at a certain date, meaning it has no awareness of ShopEase's unique and frequently updated policies. When a customer asks a specific question—for instance, about a recent change in our holiday return window—the model is forced to "guess" an answer based on general patterns it learned during training.

This leads to **hallucination**, where the LLM produces plausible-sounding but factually incorrect information because it lacks real grounding. For example, a customer might ask, "How long do I have to return a defective electronic item?" The chatbot, relying on general retail patterns, might confidently state: "You can return it within 30 days for a full refund." However, ShopEase’s actual internal policy for electronics specifies a strict **7-day return window** from the date of delivery. Such discrepancies cause significant customer frustration and operational overhead for the support team.

## Q2. What should the new assistant "read from" to give correct answers?

To ensure accuracy, the assistant should be grounded on the following internal documents:

1.  **ShopEase Global Returns & Refunds Policy** — Answers questions about return windows (e.g., 7 days for electronics vs 14 days for fashion), refund processing timelines, and restocking fees.
2.  **Product Warranty & Service Guide** — Provides details on brand-specific warranty periods, nearby authorized service centers, and the distinction between 'seller warranty' and 'manufacturer warranty'.
3.  **Shipping & Delivery Standard Operating Procedure (SOP)** — Covers delivery zones, estimated arrival times for different pin codes, and the procedure for handling missing or "marked as delivered but not received" packages.
4.  **Exchange & Replacement Workflow** — Explains the eligibility criteria for replacements (e.g., "damaged on arrival" vs "manufacturing defect") and the reverse-pickup schedule.

## Q3. Walk through the 4-step RAG flow for one realistic ShopEase customer question.

**Customer Question:** "I received a Prestige Mixer-Grinder 5 days ago, but the motor is making a burning smell. Can I still get a replacement?"

### 1. Query
The exact question from the customer is captured by the ShopEase Assistant: *"I received a Prestige Mixer-Grinder 5 days ago, but the motor is making a burning smell. Can I still get a replacement?"* This query is then converted into a numerical vector to search our knowledge base.

### 2. Retrieve
The system searches the **Returns & Replacements Policy** and retrieves the most relevant chunk.
**Retrieved Chunk:** *"For small kitchen appliances (Mixers, Grinders, Blenders), ShopEase offers a 7-day replacement-only window for manufacturing defects. If the product is reported within 7 days of delivery and shows signs of a motor defect (e.g., burning smell, failure to start), a reverse pickup will be scheduled within 48 hours for a replacement."*

### 3. Context
This retrieved chunk is placed alongside the customer’s question in a prompt sent to the LLM. The prompt looks like this: *"You are the ShopEase Support Assistant. Use the following policy snippet to answer the customer's question. Policy: [Retrieved Chunk]. Customer Question: [Query]."* This gives the LLM the specific "open-book" information it needs to be accurate.

### 4. Generate
Using the provided context, the LLM generates a grounded and helpful response.
**Assistant Answer:** "Yes, you are eligible for a replacement! According to our policy for small kitchen appliances, manufacturing defects like a burning motor smell can be reported within 7 days of delivery. Since you received your Prestige Mixer-Grinder 5 days ago, you are within the replacement window. I have initiated a reverse pickup for you, which will be completed within the next 48 hours. Once verified, we will ship your new replacement immediately."
