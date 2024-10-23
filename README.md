# Language-Learning-Assistant

A GPT-powered assistant designed to help users practice and learn a new language. This assistant supports conversation practice, vocabulary suggestions, and grammar explanations, leveraging the OpenAI API.

## Table of Contents

- [Features](#features)
- [Setup](#setup)
- [Running the Assistant](#running-the-assistant)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Vocabulary Practice**: Get definitions and example sentences for words in different languages.
- **Grammar Assistance**: Ask the assistant to explain complex grammar rules.
- **Conversation Practice**: Engage in basic conversations in the language you’re learning.
- **Daily Vocabulary Word**: Get a new word to learn every day.

## Setup

### Prerequisites

Make sure you have the following installed:

1. [Python 3.x](https://www.python.org/downloads/)
2. [Git](https://git-scm.com/)
3. OpenAI API Key ([Get your API key here](https://platform.openai.com/account/api-keys))

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/language-learning-assistant.git
cd language-learning-assistant
```

### Step 2: Set Up a Virtual Environment (Optional, but recommended)

```bash
# For Mac/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a .env file in the root directory and add your OpenAI API key:

```
OPENAI_API_KEY=your-openai-api-key
```

## Running the Assistant

Once set up, run the project using:

```bash
python app.py
```

You'll be able to ask questions, practice vocabulary, and learn grammar by interacting with the assistant.

Enter a prompt when asked, and the assistant will respond based on the language-learning tasks you request.

## Contributing

Here’s how you can contribute to the project:

### Step 1: Branching Model

Each feature should be developed in a separate branch. To create a new branch for a feature:

```bash
git checkout -b feature-name
```

Once you’ve completed your feature, push the branch and create a pull request for review:

```bash
git push origin feature-name
```

### Step 2: Pull Requests

Create a pull request (PR) when you’re ready to merge your branch.
Another teammate should review the PR before merging it into the main branch.

### Step 3: Stay in Sync

Before starting work, make sure your local repository is up to date:

```bash
git pull origin main
```

### Step 4: Commit Guidelines

Use clear and concise commit messages (e.g., Added daily vocabulary feature).
Ensure all your code is properly tested and linted before pushing.

## Contributing to the Frontend

We’ve built a simple React-based frontend to allow users to interact with the Language Learning Assistant via a browser. Here’s how you can contribute to the frontend:

### Frontend Setup

1. **Navigate to the `web-interface` directory**:

   ```bash
   cd web-interface
   ```

2. **Install the dependencies**:

   ```bash
   npm install
   ```

3. **Run the frontend development server**:

   ```bash
   npm start
   ```

   This will start the React development server, and you can access the frontend at http://localhost:3000.
