# PROJECT SPECIFICATION: The Granite Shell
# PROJECT SPECIFICATION: "The Granite Shell" (AI-Native Terminal)

## 1. Project Overview
We are building a **High-Performance Command Line Interface (CLI)** written in **C** that integrates **IBM Granite Code** (running locally via Ollama) to translate natural language user requests into executable Bash/Zsh commands.

**Goal:** Create a "smart terminal" where the user can type in plain English (e.g., "Find all PDF files larger than 10MB") and the shell executes the corresponding system command.

## 2. Tech Stack & Architecture
* **Frontend / Core Logic:** C (Standard C99/C11). Handles user input, process management, and command execution.
* **AI Backend Bridge:** Python 3.x (Intermediary). Handles the HTTP communication with the Ollama API to simplify JSON parsing.
* **AI Engine:** Ollama (Local Inference).
* **Model:** `ibm-granite/granite-code:latest` (Selected for its coding efficiency and low latency).

## 3. Data Flow (The Pipeline)
1. **Input:** User types natural language prompt into the C shell (e.g., `granite-shell > Create a backup of the src folder`).
2. **Bridge Call:** The C program invokes the Python script using a pipe or `popen()`, passing the user's string as an argument.
3. **Inference:** The Python script sends the prompt to the local Ollama endpoint (`http://localhost:11434/api/generate`).
    * *System Prompt:* "You are a Linux command expert. Translate the following request into a single executable command. Do NOT output markdown or explanations. Output ONLY the command."
4. **Translation:** IBM Granite returns the command (e.g., `tar -czvf src_backup.tar.gz src/`).
5. **Return:** Python prints the clean command to `stdout`.
6. **Capture:** The C program reads the output from the Python script.
7. **Verification:** C displays: `> Suggested Command: [command]. Execute? (Y/n)`.
8. **Execution:** If 'Y', C uses `system()` or `fork()` + `execvp()` to run the command on the OS.

## 4. Development Roadmap

### Phase 1: The AI Brain (Python + Ollama)
* **Task:** Setup Ollama with the IBM Granite Code model.
* **Deliverable:** A Python script (`brain.py`) that accepts a string arg and returns *only* the executable shell command string.

### Phase 2: The Shell Body (C Language)
* **Task:** Build the REPL (Read-Eval-Print Loop) in C.
* **Deliverable:** A C program (`shell.c`) that prints a custom prompt (`granite-shell >`), reads user input safely, and handles the loop.

### Phase 3: The Integration (IPC)
* **Task:** Connect C and Python.
* **Implementation:** Use C's `popen()` to call `python3 brain.py "user input"` and read the output stream into a C string buffer.

### Phase 4: Execution & Safety
* **Task:** Execute the command.
* **Deliverable:** Implement the execution logic using `system(cmd_buffer)` after user confirmation to prevent accidental destructive commands (like `rm -rf`).

## 5. Constraints & Philosophy
* **Local First:** Must work without internet once the model is downloaded.
* **Engineering First:** We prioritize using C for the shell to demonstrate systems programming skills (memory management, processes).
* **Model:** Must strictly use the `ibm-granite` family.

## 6. Copilot Assistant Guidelines
* **Role:** You are an expert Systems Programmer specialized in C and Linux APIs.
* **Language:** Provide explanations in **Spanish**, but keep code comments in English (industry standard).
* **C Style:** - Use strict memory management (always `free` what you `malloc`).
    - Always check for `NULL` pointers.
    - Prefer `snprintf` over `sprintf` for safety.
* **Python Style:** Follow PEP 8.
* **Context Awareness:** Always remember this is a hybrid C/Python project using Ollama locally.
