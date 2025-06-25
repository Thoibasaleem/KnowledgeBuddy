#  KnowledgeBuddy – Your AI-Powered Study Partner 

**KnowledgeBuddy** is a full-stack AI-based web platform designed to promote collaborative learning by intelligently pairing students with ideal study partners based on academic performance, backlogs, learning preferences, and subject strengths.  
It also provides real-time chat, voice messaging, file sharing, and smart study recommendations — creating a complete AI study companion.

 Built with ❤️ as part of my 3rd-year mini project using Python, Django, and  ML logic

---

##  Features

-  **AI-Based Matching** – Uses a trained **Random Forest classifier** on student data (grades, backlogs, preferences) to predict ideal study partners  
-  **Personalized Study Tips** – Uses **TF-IDF + cosine similarity** to recommend YouTube links, topics, and focus areas  
-  **Real-time Chat System** – Built using **Django Channels + WebSockets** for live messaging  
-  **Voice Notes & File Sharing** – Chat like WhatsApp with media features  
-  **Student Profile Management** – Custom profiles with study time, learning style, weakest/easiest subjects, etc.  
-  **Secure Login System** – Built with Django auth + PostgreSQL  
-  **Admin Dashboard** – Track student data, matches, and usage

---

## 🔧 Tech Stack

| Layer       | Tools |
|-------------|-------|
| **Frontend** | HTML, CSS, JavaScript |
| **Backend**  | Python, Django, Django Channels |
| **Database** | PostgreSQL |
| **ML Models** | Scikit-learn (Random Forest, TF-IDF) |
| **APIs/Tools** | WebSockets, Git, GitHub, VS Code |

---

##  AI/ML Breakdown

-  **Matching Algorithm**: Supervised ML model using **Random Forest** classifier trained on custom student dataset  
-  **Study Tips**: NLP-based recommendations using **TF-IDF vectorization** + **cosine similarity**  
-  **Preprocessing**: Cleaned and normalized student data from Excel for model training

---

##  Project Structure

# KnowledgeBuddy
knowledgebuddy/
│
├── students/ # App for handling student profiles, models & views
├── templates/ # HTML Templates
├── static/ # Static files (JS/CSS)
├── chat/ # Real-time chat system
├── recommendations/ # ML-based study tips
├── manage.py


## 📸 Screenshots

> AI-based study partner matching and chat platform

---![Screenshot 2025-03-25 215725](https://github.com/user-attachments/assets/dd1695a8-ddeb-419a-b64d-7e337bc3618e)


![Screenshot 2025-03-25 220215](https://github.com/user-attachments/assets/fa6fb9b3-d239-4825-9679-93acd785644d)

![Screenshot 2025-04-10 105214](https://github.com/user-attachments/assets/7e25be4a-a4d4-4812-9eb3-98e83ca1f08f)

## 📌 How to Run

1. Clone this repo  
2. Setup virtualenv and install dependencies  
3. Run server with: `python manage.py runserver`  
4. Open browser at `localhost:8000`

---

##  Author

👩‍💻 **Thoiba Saleem**  
📫 [LinkedIn](https://www.linkedin.com/in/thoiba-saleem)
| 📧 thoibasaleem389@gmail.com

---

> ⭐ Don’t forget to star this repo if you liked it!

