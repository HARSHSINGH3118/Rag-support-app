# 🤖 RAG Customer Support Assistant

Welcome to the **RAG Customer Support Assistant**, an end-to-end Retrieval-Augmented Generation (RAG) system built to streamline customer support interactions. It combines semantic retrieval, sentiment-aware response generation, escalation detection, and customer satisfaction (CSAT) tracking in a single unified app.

---

## 🌐 Live Demo

 **Deployment Link:** [https://your-streamlit-app-url](http://34.71.139.147:8000/)

 

---

##  Features

-  **Semantic Context Retrieval** using ChromaDB and Sentence Transformers
-  **Empathetic AI Response Generation** with sentiment analysis
-  **Escalation Detection System** (based on sentiment & trigger keywords)
-  **CSAT Tracking** with helpfulness feedback stored in a CSV
-  **Downloadable Feedback Log** (CSV export for analysis)
-  **Email Alert System** for escalations via Gmail SMTP
-  **Source Document Highlighting** for retrieved knowledge chunks
-  **CLI Logging** for escalations with color-coded output using Colorama

---

##  Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/rag-support-assistant.git
cd rag-support-assistant
```
### 2. Install Dependencies
```
pip install -r requirements.txt
```
### 3. Add Your Environment Variables
```
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```
Use Gmail App Passwords for secure SMTP usage.

### 4. Prepare Data
1) Create an articles/ folder.
2) Add your .txt support documents inside.

### 5. Launch the App
```
streamlit run app.py
```
##  Project Structure
```
├── app.py                      # Main Streamlit UI
├── retriever.py                # ChromaDB vector storage and retrieval
├── responder.py                # Empathetic response generation
├── sentiment.py                # Sentiment analysis logic
├── escalation.py               # Escalation checker with logging + email
├── utils.py                    # File loading + chunking utilities
├── articles/                   # Your knowledge base (text files)
├── db/                         # ChromaDB persistent storage
├── feedback_log.csv            # Stores user feedback (auto-generated)
├── escalation_log.txt          # Stores escalation alerts (auto-generated)
├── .env                        # Environment secrets (not committed)
├── .gitignore
└── requirements.txt
```
##  Summary of Approach
- The user query is semantically embedded and matched against a vector store (ChromaDB) to retrieve top-k relevant document chunks.

- The retrieved context and detected sentiment are fed into a custom response generator to generate empathetic, context-aware replies.

- Sentiment is evaluated using pretrained models and trigger keywords are matched for escalation detection.

- Alerts are logged to file and optionally emailed to a designated support address.

- CSAT feedback is collected and saved for post-session review.

##  Assumptions Made
- The support documents are available in .txt format and stored in a local folder.

- Gmail SMTP is used for email alerts; app password is pre-configured via .env.

- CSAT is binary (Yes/No) for simplicity.

- The system assumes a single-agent session and does not persist per-user logs.

##  Security & Privacy Notes
- .env is listed in .gitignore to protect secrets

- Email alerts use secure SSL with Gmail SMTP (port 465)

- Data is stored locally in CSV logs and ChromaDB

- No user PII is collected or transmitted externally

## Screenshot 
<img width="2551" height="1058" alt="Screenshot 2025-08-02 021119" src="https://github.com/user-attachments/assets/0e26c9e6-fa18-416b-bf5d-0194fb7295b7" />
<img width="1445" height="562" alt="Screenshot 2025-08-02 021250" src="https://github.com/user-attachments/assets/13c196cc-9597-4db4-9f53-76a4ceffe18d" />
<img width="767" height="425" alt="Screenshot 2025-08-02 021323" src="https://github.com/user-attachments/assets/970d4329-13bf-4aa2-985d-068ef2933aca" />

## Testing Instructions
-  To verify the system is working:
```
streamlit run app.py
```
- Try one of the quick questions from the sidebar
```
"How do I reset my password?"
"I want to cancel my order"
```
- Submit your own queries to:
```
Evaluate sentiment
Trigger escalation 
View retrieved support content and generated replies
```
- Try downloading the Feedback CSV from the sidebar after providing CSAT responses.

## Author
Developed by Harsh,
Final Year Computer Science Engineering Student

## License
All rights reserved © 2025.
You may fork and contribute, but for adding new features or production use, please raise a pull request and take explicit permission from the author.
