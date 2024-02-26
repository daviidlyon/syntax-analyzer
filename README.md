# Python Syntax Analyzer for LL(1) Grammars

This Python-based syntax analyzer is designed to analyze source code written in Python programming language using LL(1) grammars. It tokenizes and parses the input Python code, identifying syntactic errors and providing helpful messages for debugging and correction.

## Features

- **LL(1) Parsing:** Utilizes LL(1) parsing technique to analyze the syntax of the input Python code efficiently and accurately.
- **Error Detection:** Detects and reports syntactic errors in the input code, providing detailed information about the location and nature of the errors.
- **Python Implementation:** Implemented in Python, making it cross-platform and easy to integrate into existing Python projects.
- **Extensible:** Can be extended to support additional syntax rules or customized for specific project requirements.

## Usage

1. **Clone Repository:** Clone this repository to your local machine using the following command:

   ```
   git clone git@github.com:daviidlyon/syntax-analyzer.git
   ```

2. **Navigate to Repository:** Navigate to the cloned directory:

   ```
   cd syntax-analyzer
   ```

3. **Install Jupyter Notebook:** If you haven't already, install Jupyter Notebook using pip:

   ```
   pip install notebook
   ```

4. **Run the Jupyter Notebook:** Navigate to the cloned directory and run the Jupyter Notebook server:

   ```
   jupyter notebook
   ```

5. **Open and Run the Notebook:** Open the `syntax.ipynb` notebook and execute the code cells to test the lexical analyzer with your Small Basic source code. Alternatively, you can use manual input via stdin.

6. **Create your grammar:** If you want to use this project with another language, you have to specify the grammar, it cannot be redundant and should be suited for an LL1 analysis
