# Interactive PDF Chat Assistant

The Interactive PDF Chat Assistant is a Streamlit-powered application designed to facilitate conversations with a conversational AI model using content extracted from PDF documents. Users can upload multiple PDF files, and the application will extract the text and use it to answer questions through a user-friendly chat interface.

## Key Features

- **Multi-File Upload:** Easily upload and process multiple PDF documents at once.
- **Text Extraction:** Automatically extract text from uploaded PDF files.
- **AI-Powered Conversations:** Engage in detailed conversations with a conversational AI model trained on the extracted text.
- **Chat Interface:** Interact with the AI through an intuitive chat interface.

### Running the Application

#### Using Docker

1. **Build and Run the Docker Container:**

   ```bash
   docker compose up --build
   ```

2. **Access the Application:**

   Once the container is running, you can access the application at [http://localhost:8501](http://localhost:8501).

#### Local Development

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/kaifcoder/gemini_multipdf_chat.git
   cd gemini_multipdf_chat
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Google API Key:**

   Ensure your `.env` file contains the Google API key.

   ```plaintext
   GOOGLE_API_KEY=your_api_key_here
   ```

4. **Launch the Application:**

   ```bash
   streamlit run app.py
   ```

5. **Upload and Analyze Documents:**

   - Use the sidebar to upload PDF files.
   - Click "Process Uploads" to analyze the documents and generate embeddings.

6. **Engage in Conversations:**

   - Interact with the AI in the main chat interface to ask questions and receive detailed responses.

## Project Structure

- **app.py:** The main application script that handles document processing, AI interactions, and user interface.
- **.env:** Stores environment variables, including the Google API key.
- **requirements.txt:** Lists all the Python packages required for the application.
- **README.md:** Comprehensive documentation for the project.

## Dependencies

- **PyPDF2:** For extracting text from PDF files.
- **langchain:** For managing language models and vector stores.
- **Streamlit:** For building the user interface.
- **google.generativeai:** For accessing the Gemini AI model.
- **dotenv:** For loading environment variables from the `.env` file.

## Acknowledgments

- **Google Gemini:** Providing the advanced language model.
- **Streamlit:** Enabling the creation of interactive web applications.
