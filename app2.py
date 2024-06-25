import streamlit as st
import base64
from openai import OpenAI

st.set_page_config(
    layout="wide"
)


def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_image

def analyze_image(image_data: str) -> str:
    prompt_instruction = """
    **Instructions**:

**Identify Financial Transactions:**

-Determine and list each transaction as either a credit (money in) or a debit (money out).
-Classify each transaction into categories (e.g., salary, rent, utilities, groceries, etc.).
-Calculate Totals:

**Calculate the total amount of credits and debits.**
-Determine the net balance (total credits minus total debits).
-Analyze Monthly Data:

**Provide a breakdown of credits and debits for each month.**
-Calculate the monthly profit or loss (net balance) for each month.
-Identify any significant changes or trends in financial activity.
-Provide a Breakdown:

**Detail the total credits and debits for each category.**
-Summarize the financial activity for each month and overall.
-Summarize the Results in Brief:

**Include a brief summary of the overall financial activity.**
-Mention the total credits, total debits, and net balance.
-Highlight the key categories contributing to credits and debits.
-Provide a monthly breakdown of profit and loss.

    """

    client = OpenAI(api_key='sk-proj-J52oi8WSN')
    MODEL = "gpt-4o"

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": prompt_instruction},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}}
            ]}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content

# Streamlit UI
st.sidebar.title("Financial Data Analyzer")
uploaded_file = st.sidebar.file_uploader("Upload an image of your statement", type=["jpg", "jpeg", "png"])

if st.sidebar.button("Calculate"):
    if uploaded_file is not None:
        # Save the uploaded file
        with open("uploaded_image.png", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Encode the image
        base64_image = encode_image("uploaded_image.png")

        # Analyze the image
        result = analyze_image(base64_image)

        # Display the results
        col1, col2 = st.columns(2)
        with col1:
            st.image("uploaded_image.png", caption='Uploaded Food Order', use_column_width=True)
        with col2:
            st.markdown(result)
    else:
        st.sidebar.error("Please upload an image to proceed.")