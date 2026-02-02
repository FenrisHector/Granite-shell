# Granite Shell (AI-Native Hybrid CLI)

**Experimental command-line interface developed in C and Python that utilizes local Artificial Intelligence to translate natural language into system commands.**

## Description

This project implements a smart terminal capable of interpreting user intent expressed in natural language and executing the corresponding system operations. The architecture is built on a hybrid model: a low-level core written in **C** manages the interface, process execution, and memory, while a high-level subsystem in **Python** acts as the cognitive layer, communicating with local LLMs (Large Language Models) via **Ollama**.

The primary focus of this development was to explore **Interprocess Communication (IPC)** between compiled and interpreted languages using pipes, rather than relying on pre-built AI wrappers. The system runs on Windows but is designed to function as a hybrid environment. By default, it favors Unix-like syntax (providing a Linux feel on Windows using tools like MinGW or Git Bash), but it retains the capability to execute native Windows commands when explicitly requested by the user.

## Objectives

* **Hybrid Architecture Implementation:** Successfully integrate a C-based Read-Eval-Print Loop (REPL) with a Python-based inference script using standard input/output streams.
* **Natural Language Processing:** Enable the execution of complex file manipulation and system tasks (e.g., "create a file and write hello inside") without requiring the user to know specific syntax.
* **Local Inference:** Utilize Ollama to run the AI model locally, ensuring privacy and eliminating latency associated with cloud APIs.
* **Response Parsing:** Develop robust regular expressions (Regex) in Python to sanitize AI outputs, ensuring only executable code is returned to the C shell.

## Operational Constraints & Hybrid Behavior

It is important to note the specific operational logic of this shell regarding the Windows environment:

* **Unix-First Approach:** The AI model is prompted to prefer standard Unix commands (such as `ls`, `grep`, `cat`). For this to function correctly on Windows, the host machine must have a set of Unix tools in the system PATH (e.g., via w64devkit, MinGW, or Git Bash).
* **Windows Native Commands:** To execute specific Windows commands (like `dir`, `winget`, or `ipconfig`), the user must explicitly specify the operating system in the prompt.
    * *Example:* "List files" will trigger `ls -la`.
    * *Example:* "List files using windows command" will trigger `dir`.
* **Single-Line Execution:** For security and stability reasons, the shell is currently limited to executing single-line commands returned by the API.

## Methodology

### 1. The Core (C)
The `main.c` file serves as the body of the application. It handles the user input loop, manages memory buffers for command strings, and utilizes `popen()` to spawn the Python interpreter as a subprocess. It also handles ANSI color coding for visual feedback (Green for success, Red for errors).

### 2. The Brain (Python)
The `brain.py` script acts as the bridge to the AI. It receives the raw string from the C executable, constructs a JSON payload, and sends a POST request to the local Ollama instance. It parses the JSON response, strips Markdown formatting, and returns clean command text.

### 3. Safety & Parsing
The system implements a "fail-safe" mechanism. If the AI returns conversational text instead of code, the Python script filters this out to prevent syntax errors in the terminal.

## Repository Structure

```
Granite-Shell/
├── bin/
│   └── gshell.exe         # Compiled binary executable
├── bridge/
│   └── brain.py           # Python script for AI communication
├── src/
│   └── main.c             # Source code for the C shell core
└── README.md              # Project documentation
```

## Technologies

* **Core Language:** C (Standard C99)
* **Scripting Language:** Python 3.x
* **AI Engine:** Ollama (running local models such as IBM Granite or Llama 3)
* **Dependencies:**
  * `gcc` (GNU Compiler Collection) for compilation.
  * Python libraries: `requests`, `sys`, `re`.
  * Unix-tools for Windows (w64devkit/MinGW recommended).

## Execution

### 1. Prerequisites
* Ensure **Ollama** is installed and running on port `11434`.
* You must have a model pulled (e.g., `ollama pull granite-code`).
* Ensure **Python** and **GCC** are added to your system PATH.

### 2. Compilation
To compile the C core, navigate to the project root and run:

```bash
mkdir bin
gcc src/main.c -o bin/gshell.exe
```

### 3. Running the Shell
Launch the executable from the terminal:

```bash
.\bin\gshell.exe
```
## Author

**Hector Zamorano Garcia**

## Notes

* This project was developed for educational purposes to demonstrate the interoperability between low-level system programming and modern AI APIs.
* The project requires an active local instance of Ollama to function.
* Occasional AI assistance was used for generating regex patterns and debugging syntax errors during the development of the Python bridge.
