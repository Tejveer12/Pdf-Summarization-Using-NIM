import streamlit as st
import fitz

from openai import OpenAI

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)


def read_pdf(pdf_file):
    text = ""
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text


def summarize(text):
    try:
        response = client.chat.completions.create(
            model="google/gemma-2-27b-it", # Change LLM Model
            messages=[{"role": "user", "content": f"Create a summary from below text in 100 words {text}"}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
        )

        summary = response.choices[0].message.content
        return summary
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return ""


def main():
    st.title("PDF Uploader and Summarizer")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        st.subheader("PDF Content")
        text = read_pdf(uploaded_file)

        st.text_area("Extracted Text", text, height=300)

        if st.button("Summarize"):
            with st.spinner("Summarizing..."):
                summary = summarize(text)
                st.subheader("Summary")
                st.markdown(summary)
                #st.text_area("Summary", summary, height=300)

if __name__ == "__main__":
    main()
