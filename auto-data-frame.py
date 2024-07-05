import pandas as pd
import re
from llama_cpp import Llama
import torch
from torch import mps

device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")

code_model = Llama.from_pretrained(
    repo_id="TheBloke/CodeLlama-7B-Instruct-GGUF",
    filename="*Q5_K_M.gguf",
    verbose=0,
    device=device,
)

chat_model = Llama.from_pretrained(
    repo_id="IlyaGusev/saiga_llama3_8b_gguf",
    filename="*q8_0.gguf",
    verbose=0,
    device=device,
)

class AutoDataFrame(pd.DataFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def __get_columns_description(self):
        text_description = ", ".join([f"{col}: {self[col].dtype}" for col in self.columns])
        max_tokens = 100
        if len(text_description.split()) > max_tokens:
            text_description = ' '.join(text_description.split()[:max_tokens])
        return text_description

    def __generate_algorithm(self, task):
        cols_description = self.__get_columns_description()
        data_sample = self.head(1).to_string()
        
        prompt = (f"user: Сделай формулировку задачи более развернутой и переведи на английский, "
                  f"также добавь в условие описание датасета: {cols_description}. Вот условие задачи: {task}. "
                  f"Пример данных:\n{data_sample}\n"
                  "bot:")
        
        output = chat_model(
            prompt,
            temperature=0.7,
            top_p=1,
            max_tokens=300,
            echo=False
        )
        return output['choices'][0]['text']

    def __generate_code_variant(self, prompt):
        try:
            output = code_model(
                prompt,
                temperature=0.7,
                top_p=1,
                max_tokens=1500,
                echo=False
            )
            return output['choices'][0]['text']
        except Exception as e:
            print(f"Error in generate_code_variant: {e}")
            return None

    def __generate_code_variants(self, task, num_variants=3):
        prompt = (f"[INST] Write Python code using pandas to solve the following problem. Ensure the code adheres to best practices, "
                  f"handles edge cases, and is well-commented. Here is the detailed problem description: {task} "
                  "The final function should accept the dataset as input and return answer\n[/INST]\n")

        variants = []
        for _ in range(num_variants):
            result = self.__generate_code_variant(prompt)
            if result:
                variants.append(result)
        
        return variants

    def __evaluate_code_variant(self, code, task, cols_description):
        prompt = (f"user: The following code was generated for a specific problem description. "
                  f"Please evaluate if the code correctly solves the problem based on the given task and dataset description. "
                  f"Task: {task}\n"
                  f"Dataset Description: {cols_description}\n"
                  f"Generated code:\n```python\n{code}\n```\n"
                  "Provide a score between 0 and 10, with 10 being the best. Also, give a brief explanation of your score.\n"
                  "bot:")

        output = chat_model(
            prompt,
            temperature=0.7,
            top_p=1,
            max_tokens=512,
            echo=False
        )
        response = output['choices'][0]['text']
        
        match = re.search(r'\b\d{1,2}\b', response)
        score = int(match.group()) if match else 0
        return code, score, response

    def __evaluate_code_variants(self, variants, task, cols_description):
        evaluations = []
        for code in variants:
            evaluations.append(self.__evaluate_code_variant(code, task, cols_description))

        best_code = max(evaluations, key=lambda x: x[1])[0]
        return best_code
    
    def __validate_code_format(self, generated_code):
        prompt = (f"user: Please review the following code to ensure it adheres to standard coding practices and formatting. "
                "If there are any issues, correct them and provide the updated code. In answer must be only function code, which return value."
                "This function must be called get_stat()"
                f"Generated code:\n```python\n{generated_code}\n```\nbot: \n")
        
        output = chat_model(
            prompt,
            temperature=0.7,
            top_p=1,
            max_tokens=1500,
            echo=False
        )
        return output['choices'][0]['text']

    def generate_code(self, task):
        try:
            cols_description = self.__get_columns_description()
            detailed_task = self.__generate_algorithm(task)
            
            code_variants = self.__generate_code_variants(detailed_task)
            best_code = self.__evaluate_code_variants(code_variants, detailed_task, cols_description)
            
            validated_code = self.__validate_code_format(best_code)
            
            return validated_code
        except Exception as e:
            print(f"Error in generate_statistic: {e}")
            return None
        
    def extract_python_code(self, text):
        pattern = r'```python\n(.*?)\n```'
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1) if match else ""
        
    def get_statistic(self, prompt):
        task = prompt + "Итоговая функция должна возвращать число"
        сode = self.generate_code(task)
        
        return self.extract_python_code(сode)
    
    def change_table(self, prompt):
        task = prompt + "Итоговая функция должна возвращать измененый датасет"
        сode = self.generate_code(task)
        
        return self.extract_python_code(сode)
    
    def plot_by_promt(self, prompt):
        task = prompt + "Итоговая функция должна возвращать объект графика matplotlib"
        сode = self.generate_code(task)
        
        return self.extract_python_code(сode)


def read_csv(*args, **kwargs):
    df = pd.read_csv(*args, **kwargs)
    return AutoDataFrame(df)


def read_excel(*args, **kwargs):
    df = pd.read_excel(*args, **kwargs)
    return AutoDataFrame(df)
