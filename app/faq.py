import pandas as pd
from pathlib import Path
import chromadb
from openai import OpenAI
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import os

# SETTING UP THE ENV
load_dotenv()
#os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

faqs_path=Path(__file__).parent/"resources/faq_data.csv"

if not faqs_path.exists():
    raise FileNotFoundError(f"FAQ file not found at: {faqs_path} ")

# CREATING CHROMA CLIENT
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection_name_faq="faqs"
ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small")

openai_client=OpenAI()

def ingest_faq_data(path):
    if collection_name_faq not in [c.name for c in chroma_client.list_collections()]:
        print("Ingesting the data into Chromadb....")
        collection=chroma_client.get_or_create_collection(name=collection_name_faq,
                                               embedding_function=ef)
        df=pd.read_csv(path)
        docs=df["question"].to_list()
        metadata=[{"answer":ans} for ans in df["answer"].to_list()]
        ids=[f"id_{i}" for i in range(len(docs))]

        collection.add(documents=docs,
                       metadatas=metadata,
                       ids=ids)
    else:
        print(f"Collection {collection_name_faq} already exists!")

def get_relevant_qa(query):
    collection=chroma_client.get_collection(name=collection_name_faq,embedding_function=ef)
    result=collection.query(
        query_texts=[query],
        n_results=2)
    return result

def faq_chain(query):
    result=get_relevant_qa(query)
    context="\n\n".join([r.get("answer") for r in result["metadatas"][0]])
    answer=generate_answer(query,context)
    return answer
def generate_answer(query,context):
    prompt=f'''Given the question and context below, generate the answer based
    on the context only. if you dont know the answer, say I dont know. Dont make things up
    QUESTION:{query}
    CONTEXT:{context}
    '''
    chat_completion = openai_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
    )

    return chat_completion.choices[0].message.content


if __name__=="__main__":
    ingest_faq_data(faqs_path)
    print("FAQ Bot ready! Type 'quit' to exit.")
    while True:
        query = input("\nAsk a question: ")
        if query.lower() in ["quit", "exit"]:
            break
        answer = faq_chain(query)
        print(f"\nAnswer: {answer}")