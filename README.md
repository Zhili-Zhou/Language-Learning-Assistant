# Language-Learning-Assistant

A GPT-powered assistant designed to help users practice and learn a new language. This assistant supports conversation practice, vocabulary suggestions, and grammar explanations, leveraging the OpenAI API.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Contributing](#contributing)
- [API Usage](#api-usage)

## Features

- **Translation Assistance**: Get unfamiliar words translated.
- **Vocabulary Practice**: Get definitions and example sentences for words in different languages.
- **Grammar Assistance**: Ask the assistant to explain complex grammar rules.
- **Pronunciation Assistance**: Get the pronunciation of the words/sentences.
- **Daily Vocabulary Word**: Get a new word to learn every day.

## Project Structure

```
/Language-Learning-Assistant
│
├── /backend
│   ├── app.py                   # Flask backend core logic
│   ├── assistant_config.json    # Configuration file for Assistant
│   └── requirements.txt         # Python dependencies required for the backend
│
├── /venv                        # Virtual environment folder (not committed to GitHub)
│
├── /web-interface               # Frontend folder
│   ├── /node_modules            # Node.js dependencies (not committed to GitHub)
│   ├── package-lock.json        # Locks the versions of frontend dependencies
│   ├── package.json             # Lists the required frontend dependencies
│   ├── /public
│   │   └── index.html           # Main HTML file for the frontend
│   ├── /src
│   │   ├── app.js               # Main React component
│   │   ├── /components          # Reusable React components
│   │   ├── index.css            # Main CSS file for styling
│   │   └── index.js             # Entry JavaScript file that renders the React app
│
├── README.md                    # Project documentation
└── .gitignore                   # Git ignore file (to ignore sensitive files like .env and node_modules)


```

## Setup Instructions

### Prerequisites

Make sure you have the following installed:

- [Python 3.x](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- OpenAI API Key ([Get your API key here](https://platform.openai.com/account/api-keys))
- Node.js (version 14+ recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/language-learning-assistant.git
cd language-learning-assistant
```

### Step 2: Backend Setup

#### 1. Set Up a Virtual Environment (Optional, but recommended)

```bash
# For Mac/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Add your OpenAI API Key in a .env file in the backend folder:

Create a .env file in the root directory and add your OpenAI API key:

```
OPENAI_API_KEY=your-openai-api-key
```

#### 4. Run the Flask server:

```
python backend/app.py
```

The backend server will run on http://127.0.0.1:5000

### Step 3: Frontend Setup

#### 1. Navigate to the frontend/ folder:

```bash
cd web-interface
```

#### 2. Install the dependencies:

If you have already installed, please skill this part.

```bash
npm install
```

#### 3. Create a .env file in the frontend/ folder::

Normally it should be already there.

```bash
REACT_APP_BACKEND_URL=http://127.0.0.1:5000
```

#### 4. Run the frontend development server:

```
npm start

```

This will start the React development server, and you can access the frontend at http://localhost:3000

You'll be able to ask questions, practice vocabulary, and learn grammar by interacting with the assistant.

Enter a prompt, and the assistant will respond based on the language-learning tasks you request.

### Step 4: Running the Application

With both the backend and frontend servers running, open http://localhost:3000 in your browser to start using the Language Learning Assistant.

## Contributing

Here’s how you can contribute to the project:

1. **Fork the repository and clone it to your local machine.**

2. **Create a new branch for your feature or fix:**

   ```
   git checkout -b feature/my-new-feature
   ```

   Make your changes in the codebase.

3. **Commit your changes:**

   ```
   git commit -m "Add my new feature"
   ```

4. **Push to your branch:**

   ```
   git push origin feature/my-new-feature
   ```

   Create a Pull Request on GitHub and request a review from a teammate.

## API Usage

The project interacts with OpenAI's GPT models via the API. The core of the interaction happens in the /ask endpoint in the backend:

POST /ask: Sends a user message to the assistant and receives a response.

Example request body:

```
{
  "message": "Translate 'good morning' to French",
  "assistant": "language"
}
```

Example response:

```
{
  "answer": "Good morning in French is 'Bonjour'."
}

```
