from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer, T5Tokenizer, T5ForConditionalGeneration
import os
import requests
import json

summary_model = pipeline("summarization",model="facebook/bart-large-cnn")
translation_model = pipeline("translation_en_to_fr",model="Helsinki-NLP/opus-mt-en-fr")
#use google-t5/t5-base
# translation_tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-xxl")
# translation_model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-xxl")


expansion_model = pipeline("text-generation",model="gpt2-medium")
fact_check_model = pipeline("question-answering",model="deepset/roberta-base-squad2")
# fact_check_model = pipeline("zero-shot-classification",model="gpt2-medium")

def summarize(text):
    summary = summary_model(text, max_length=60, min_length=20, do_sample=False)
    return summary[0]['summary_text']

def translate(text):
    # Assuming the target language is French for simplicity
    translation = translation_model(text)
    return translation[0]['translation_text']

def expand(text):
    expansion = expansion_model(text, max_length=200, num_return_sequences=1)
    return expansion[0]['generated_text']

def fact_check(statement):
    context = "The Earth orbits the Sun. The Sun rises in the East and sets in the West. The Earth is round."
    question = f"Is it true that {statement}?"
    result = fact_check_model(question=question, context=context)
    return result['answer']

def save_output(output, filename):
    with open(filename, 'w') as file:
        file.write(output)
    print(f"Output saved to {filename}")

def main():
    while True:
        print("\nPlease select a task:")
        print("1. Summarize text")
        print("2. Translate text to another language")
        print("3. Expand text")
        print("4. Fact-check text")

        task = input("Enter the task number (1-4): ")

        if task == "1":
            text = input("\nPlease enter the text to summarize:\n")
            output = summarize(text)
            print("\nSummary:\n", output)
            
        elif task == "2":
            text = input("\nPlease enter the text to translate:\n")
            output = translate(text)
            print("\nTranslation:\n", output)

        elif task == "3":
            prompt = input("\nPlease enter the prompt:\n")
            output = expand(prompt)
            print("\nGenerated text:\n", output)
        
        elif task == "4":
            statement = "Is it true or false that " +input("\nPlease enter the statement to fact-check:\n") + "? Why or why not explain?"
            output = fact_check(statement)
            print("\n", output)
        
        else:
            print("Invalid task number. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()

