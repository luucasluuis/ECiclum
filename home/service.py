import google.generativeai as genai
import pandas as pd
import os

# Defina a chave da API da OpenAI
#openai.api_key = os.getenv("OPENAI_API_KEY")

dados_vendas = pd.DataFrame({
    'data': ["2024-01-01", "2024-01-01", "2024-01-02", "2024-01-02", "2024-01-03"],
    'horario': ["09:00", "15:00", "11:00", "18:00", "13:00"],
    'produto': ["Arroz", "Feijão", "Macarrão", "Arroz", "Azeite"],
    'quantidade': [2, 5, 3, 4, 2]
}).to_json()

def gerar_insights(data=dados_vendas):

    api_key = ""
    genai.configure(api_key=api_key)

    try:
        prompt = (
            f"Baseado nos dados de vendas a seguir:\n{data}\n"
            "Quais padrões de compra você observa em termos de dias da semana e horários do dia?"
        )
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro ao gerar insights: {e}"

# Carregar dados históricos de vendas (exemplo fictício)

if __name__ == "__main__":
    print(gerar_insights(dados_vendas))
