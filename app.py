import requests 
import time
import sys

API_URL = "https://api-inference.huggingface.co/models/"
API_KEY = "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"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

# Function to get output from the model
def get_output(model, input_json):
    response = requests.post(f"{API_URL}{model}", headers=headers, json=input_json)
    return response.json()

# Function to summarize text
def summarize_text(model, input_json, file_name):
    output = get_output(model, input_json)
    try:
        # Save the summary to a file
        if file_name:
            with open(file_name, "w") as f:
                f.write(output[0]["summary_text"])
                print(f"\nSummary saved to {file_name}")
        else:
            print("\nSummary:\n" + output[0]["summary_text"])
    except:
        try:
            # Handle estimated time for processing
            t = output['estimated_time']
            time.sleep(5)      #we wait for a few seconds before making http request again so that we dont get blocked
            summarize_text(model, input_json)
        except:
            # Handle model service not available
            print("Model service not available. Please try again later.")

# Function to translate text
def translate_text(model, input_json, file_name):
    output = get_output(model, input_json)
    try:
        try:
            # Save the translation to a file (remove suggestions and improvements)
            if file_name:
                with open(file_name, "w") as f:
                    f.write(output[0]["generated_text"].split("improvements.")[1].strip())
                    print(f"\nTranslation saved to {file_name}")
            else:
                print("\nTranslation:\n" + output[0]["generated_text"].split("improvements.")[1].strip())
        except:
            # Save the translation to a file
            if file_name:
                with open(file_name, "w") as f:
                    f.write(output[0]["generated_text"])
                    print(f"\nTranslation saved to {file_name}")
            else:
                print("\nTranslation:\n" + output[0]["generated_text"])
    except:
        try:
            # Handle estimated time for processing
            t = output['estimated_time']
            time.sleep(5)
            translate_text(model, input_json)
        except:
            print("\nModel service not available. Please try again later.")

# Function to generate (expand) text
def generate_text(model, input_json, file_name="generation.txt"):
    output = get_output(model, input_json)
    try:
        # Save the generated text to a file
        if file_name:
            with open(file_name, "w") as f:
                f.write(output[0]["generated_text"])
                print(f"\nGenerated text saved to {file_name}")
        else:
            print("\nGenerated text:\n" + output[0]["generated_text"])
    except:
        try:
            # Handle estimated time for processing
            t = output['estimated_time']
            time.sleep(5)
            generate_text(model, input_json)
        except:
            print("Model service not available. Please try again later.")

# Function to fact-check text
def fact_check(model, input_json, file_name="fact_check.txt"):
    output = get_output(model, input_json)
    try:
        try:
            #save the answer to a file (remove the question)
            if file_name:
                with open(file_name, "w") as f:
                    f.write(output[0]['generated_text'].split("?")[1].strip())
                    print(f"\nFact-check saved to {file_name}")
            else:
                print("\nFact-check:\n" + output[0]['generated_text'].split("?")[1].strip())
        except:
            #save the answer to a file
            if file_name:
                with open(file_name, "w") as f:
                    f.write(output[0]['generated_text'])
                    print(f"\nFact-check saved to {file_name}")
            else:
                print("\nFact-check:\n" + output[0]['generated_text'])
    except:
        try:
            # Handle estimated time for processing
            t = output['estimated_time']
            time.sleep(5)
            fact_check(model, input_json)
        except:
            print("Model service not available. Please try again later.")

            

# Main function to run the console application
def main(file_name=None):

    # Check if an output file name is provided correctly
    if file_name:
        if not file_name.endswith(".txt"):
            file_name += ".txt"
        print(f"Output will be saved to {file_name}")

    # Main loop to select a task
    while True:
        # Prompt user to select a task

        time.sleep(1) #we wait for a second for every request for the user to see the output

        print("\nPlease select a task:")
        print("1. Summarize text")
        print("2. Translate text to another language")
        print("3. Expand text")
        print("4. Fact-check text")
        print("5. Exit the program\n")

        task = input("Enter the task number (1-5): ")

        if task == "1":
            # Summarize text
            model = "sshleifer/distilbart-cnn-12-6"
            text = input("\nPlease enter the text to summarize:\n")
            input_json = {
                "inputs": text
            }
            summarize_text(model, input_json, file_name)

        elif task == "2":
            # Translate text
            model = "mistralai/Mistral-7B-Instruct-v0.2"
            text = input("\nPlease enter the text to translate:\n") + " and only give the translated text with no suggestions and improvements."
            input_json = {
                "inputs": text
            }
            translate_text(model, input_json, file_name)

        elif task == "3":
            # Expand text
            prompt = input("\nPlease enter the prompt:\n")
            model = "mistralai/Mistral-7B-Instruct-v0.2"
            input_json = {
                "inputs": prompt
            }
            generate_text(model, input_json, file_name)
        
        elif task == "4":
            # Fact-check text
            text = input("\nPlease enter the text to fact-check:\n")
            model = "mistralai/Mistral-7B-Instruct-v0.2"
            input_json = {
                "inputs": "Answer me if it is true or false that " + text + " ?"
            }
            fact_check(model, input_json, file_name)
        
        elif task == "5":
            break

        else:
            print("\nInvalid task number. Please try again.")

if __name__ == "__main__":
    #output file name: python3 app.py output.txt
    file_name = None
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    main(file_name)
