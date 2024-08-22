from langchain_core.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain_community.chat_models import ChatOllama

# text="""
# People across the country, involved in government, political, and social activities, are dedicating their time to make the ‘Viksit Bharat Sankalp Yatra’ (Developed India Resolution Journey) successful. Therefore, as a Member of Parliament, it was my responsibility to also contribute my time to this program. So, today, I have come here just as a Member of Parliament and your ‘sevak’, ready to participate in this program, much like you.

# In our country, governments have come and gone, numerous schemes have been formulated, discussions have taken place, and big promises have been made. However, my experience and observations led me to believe that the most critical aspect that requires attention is ensuring that the government’s plans reach the intended beneficiaries without any hassles. If there is a ‘Pradhan Mantri Awas Yojana’ (Prime Minister’s housing scheme), then those who are living in jhuggis and slums should get their houses. And he should not need to make rounds of the government offices for this purpose. The government should reach him. Since you have assigned this responsibility to me, about four crore families have got their ‘pucca’ houses. However, I have encountered cases where someone is left out of the government benefits. Therefore, I have decided to tour the country again, to listen to people’s experiences with government schemes, to understand whether they received the intended benefits, and to ensure that the programs are reaching everyone as planned without paying any bribes. We will get the real picture if we visit them again. Therefore, this ‘Viksit Bharat Sankalp Yatra’ is, in a way, my own examination. I want to hear from you and the people across the country whether what I envisioned and the work I have been doing aligns with reality and whether it has reached those for whom it was meant.

# It is crucial to check whether the work that was supposed to happen has indeed taken place. I recently met some individuals who utilized the Ayushman card to get treatment for serious illnesses. One person met with a severe accident, and after using the card, he could afford the necessary operation, and now he is recovering well. When I asked him, he said: “How could I afford this treatment? Now that there is the Ayushman card, I mustered courage and underwent an operation. Now I am perfectly fine.”  Such stories are blessings to me.

# The bureaucrats, who prepare good schemes, expedite the paperwork and even allocate funds, also feel satisfied that 50 or 100 people who were supposed to get the funds have got it. The funds meant for a thousand villages have been released. But their job satisfaction peaks when they hear that their work has directly impacted someone’s life positively. When they see the tangible results of their efforts, their enthusiasm multiplies. They feel satisfied. Therefore, ‘Viksit Bharat Sankalp Yatra’ has had a positive impact on government officers. It has made them more enthusiastic about their work, especially when they witness the tangible benefits reaching the people. Officers now feel satisfied with their work, saying, “I made a good plan, I created a file, and the intended beneficiaries received the benefits.” When they find that the money has reached a poor widow under the Jeevan Jyoti scheme and it was a great help to her during her crisis, they realise that they have done a good job. When a government officer listens to such stories, he feels very satisfied.

# There are very few who understand the power and impact of the ‘Viksit Bharat Sankalp Yatra’. When I hear people connected to bureaucratic circles talking about it, expressing their satisfaction, it resonates with me. I’ve heard stories where someone suddenly received 2 lakh rupees after the death of her husband, and a sister mentioned how the arrival of gas in her home transformed her lives. The most significant aspect is when someone says that the line between rich and poor has vanished. While the slogan ‘Garibi Hatao’ (Remove Poverty) is one thing, but the real change happens when a person says, “As soon as the gas stove came to my house, the distinction between poverty and affluence disappeared.
# """


import base64

def decode_base64(encoded_string: str) -> str:
    """
    Decodes a Base64 encoded string.

    Args:
        encoded_string (str): The Base64 encoded string.

    Returns:
        str: The decoded string.

    Raises:
        ValueError: If the input is not a valid Base64 encoded string.
    """
    try:
        # Ensure the string is valid Base64
        decoded_bytes = base64.b64decode(encoded_string, validate=True)
        decoded_string = decoded_bytes.decode('utf-8')
        return decoded_string
    except base64.binascii.Error as e:
        raise ValueError("Invalid Base64 encoding.") from e
    except UnicodeDecodeError as e:
        raise ValueError("Decoded bytes could not be converted to a string.") from e

# Example usage
if __name__ == "__main__":
    encoded_string = "UHl0aG9uIGlzIGdyZWF0IQ=="
    try:
        decoded_string = decode_base64(encoded_string)
        print("Decoded string:", decoded_string)
    except ValueError as e:
        print("Error:", e)


async def generate_summary(text:str):

    try:
        llm = ChatOllama(model="llama3.1:8b")
        
        docs = [Document(page_content=text)]

        template = '''Write a concise and short summary of the following content.
        Content: `{text}`
        '''
        prompt = PromptTemplate(
            input_variables=['text'],
            template=template
        )

        chain = load_summarize_chain(
        llm,
        chain_type='stuff',
        prompt=prompt,
        verbose=False
        )

        output_summary = chain.invoke(docs)

        if output_summary and output_summary["output_text"]:
            return output_summary["output_text"]
        else:
            return None
        
    except Exception as e:
        print(e)