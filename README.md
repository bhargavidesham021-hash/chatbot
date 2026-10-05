# AI Viva Practice Room

A simple Python and Streamlit app that uses Ollama with the `llama3.2` model to generate five project-specific viva questions and evaluate answers out of 10.

## Run locally

1. Install [Ollama](https://ollama.com/download) and start it.
2. Download the model in a terminal:

   ```powershell
   ollama pull llama3.2
   ```

3. Install the Python dependencies from the project folder:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Start the Streamlit app:

   ```powershell
   python -m streamlit run app.py
   ```

No API key is needed. Keep Ollama running while using the app.

## Push to GitHub

Push the project files, including `app.py`, `requirements.txt`, and this README. GitHub stores the source code; it does not run the app or provide access to Ollama on your computer. To run the app on another computer, install Ollama there and download `llama3.2` as described above. A cloud deployment also needs an Ollama server that the deployed app can reach.
