import os
import openai
from together import Together
from dotenv import load_dotenv

load_dotenv("chaves.env")

def gerar_resumo_ia(resumo_estatistico: str, model_provider: str = "together", contexto_negocio: str = "") -> str:
    """
    Gera um resumo usando LLM, com suporte a Together ou OpenAI.
    """
    prompt = (
        "Você é um assistente de business intelligence experiente e orientado a negócios digitais. "
        "Com base no resumo estatístico abaixo, faça uma análise clara e útil, incluindo:\n"
        "- Principais tendências ou mudanças que merecem atenção\n"
        "- Padrões interessantes ou incomuns\n"
        "- Alertas para possíveis problemas ou oportunidades\n"
        "- Recomendações práticas para decisões de negócio e em produtos digitais\n"
        "- Seja sucinto, evite números e foque mais na mensagem, como um jornalista, imagine que seu público não é familiarizado com dados\n\n"
    )
    
    if contexto_negocio:
        prompt += f"Contexto do negócio:\n{contexto_negocio}\n\n"
        
    prompt += f"Resumo dos dados:\n{resumo_estatistico}"

    if model_provider == "together":
        try:
            together_api_key = os.getenv("TOGETHER_API_KEY")
            together = Together(api_key=together_api_key)
            response = together.completions.create(
                prompt=prompt,
                model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                max_tokens=450,
                temperature=0.6,
            )
            return response.choices[0].text.strip()
        except Exception as e:
            return f"Erro ao gerar resumo com Together: {e}"

    elif model_provider == "openai":
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Você é um analista de dados."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            return response.choices[0].message["content"]
        except Exception as e:
            return f"Erro ao gerar resumo com OpenAI: {e}"

    else:
        return "Erro: provedor de modelo não reconhecido."
