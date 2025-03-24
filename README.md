# Galaxy of AI - Open Source Django Backend

Welcome to the **Galaxy of AI** backend repository! This open-source Django-based backend powers our AI/ML research and collaboration platform, providing APIs and services for AI enthusiasts, researchers, and developers.

## 🌌 About Us
**Galaxy of AI** is an open-source platform designed for AI/ML, NLP, and Generative AI (LLMs) enthusiasts. Our mission is to foster collaboration, accelerate AI research, and help developers stay ahead of technological advancements.

## 🚀 Our Mission
We aim to empower the developer community by offering:
- High-quality tutorials and research articles 📚
- Real-world AI project collaborations 🤝
- Open-source contributions to advance AI research and development 🔬

By staying updated with the latest AI trends, tools, and research, we strive to shape the future of AI development.

## 🛠️ Tech Stack
This Django backend is built with the following technologies:
- **Python** 🐍
- **Django** 🏗️
- **Django REST Framework (DRF)** 🌐
- **PostgreSQL / MySQL** 🗄️
- **Celery & Redis** (for task queues) ⏳
- **JWT Authentication** 🔐

## 📜 Features
- User authentication & JWT-based authorization
- AI model management & API endpoints
- Research article & knowledge-sharing APIs
- Task queue & background processing
- Scalable & modular architecture

## 📦 Installation & Setup
Follow these steps to set up the Django backend locally:

### 1️⃣ Clone the repository
```bash
git clone https://github.com/merhasmukh/Galaxy-Of-AI-API-Hub.git
cd Galaxy-Of-AI-API-Hub
```

### 2️⃣ Set up a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure environment variables
Create a `.env` file and set the required environment variables:
```ini
SECRET_KEY=your_secret_key
DEBUG=True
```

### 5️⃣ Apply database migrations
```bash
python3 manage.py migrate
```

### 6️⃣ Run the development server
```bash
python3 manage.py runserver
```

## 🛠️ API Endpoints
To explore the available API endpoints, use Django's browsable API or tools like Postman.
```bash
http://127.0.0.1:8000/swagger/
```

## 🤝 Contributing
We welcome open-source contributions! To contribute:
1. Fork the repository 🍴
2. Create a feature branch (`git checkout -b feature-xyz`) 🛠️
3. Commit your changes (`git commit -m "Add feature xyz"`) ✅
4. Push to your branch (`git push origin feature-xyz`) 🚀
5. Open a Pull Request 📩

## 📜 License
This project is licensed under the **Public License**.

## 📩 Contact & Community
- 🌐 Website: [Galaxy of AI](https://galaxyofai.com)
- 📧 Email: galaxyofai.com@gmail.com
---

© 2024 Galaxy Of AI. All Rights Reserved.

