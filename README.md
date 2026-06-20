# Arquitetura
                    +----------------+
                    | Burp Suite     |
                    | Jython 2.7     |
                    +--------+-------+
                             |
                             | HTTP localhost
                             |
                             V
                    +----------------+
                    | Python 3.12    |
                    | AI Service     |
                    | FastAPI/Flask  |
                    +--------+-------+
                             |
                             | OpenAI SDK
                             |
                             V
                    +----------------+
                    | OpenAI API     |
                    +----------------+


# Instruções de Instalação
## 1. Configurar o Serviço Python 3
bash

## Clone o repositório
```
git clone https://github.com/orestescaminha/ChatGPT_Burp-Extension-v1.git
cd ChatGPT_Burp-Extension-v1
```

## Crie um ambiente virtual
```
python3.12 -m venv venv
source venv/bin/activate  # Linux/Mac
```
ou
```
venv\Scripts\activate  # Windows
```
OBS: Evite erros! Use Python 3.12 que tem melhor suporte para dependências Rust-compiladas. O pydantic-core 2.14.1 foi testado com Python 3.12 e anteriores.

## Instale dependências
```
pip install -r ai_service/requirements.txt
```
## Configure a chave de API
```
export OPENAI_API_KEY="sk-..."
```
## Inicie o serviço
```
python ai_service/main.py
```
Será executado em http://127.0.0.1:8000

---

## 2. Baixe e importe o arquivo Jython standalone JAR
Jython (incluindo jython-standalone-2.7.4.jar) é compatível com Python 2.7, não com Python 3. Aqui, ele não executa o SDK da OpenAI dentro do Burp. Em vez disso, o Burp atua como cliente e um processo Python 3 separado faz a comunicação com a API.
Você precisará baixá-lo e configurá-lo no Burp Suite.
Passos para baixar e configurar o Jython:
```
Acesse a página de downloads do Jython (https://www.jython.org/download).
Baixe o arquivo .jar independente do Jython (por exemplo, jython-standalone-2.7.4.jar).
Abra o Burp Suite.
Acesse a aba Extensions no Burp Suite.
Na aba Options, role para baixo até a seção Python Environment*.
Clique em Select File e escolha o arquivo jython-standalone-2.7.4.jar que você acabou de baixar.
Clique em Apply para carregar o ambiente Jython no Burp Suite.
```
---

## 3. Carregue a Extensão no Burp

    Vá em Extender > Extensions > Add
    Tipo: Python
    Arquivo: burp_extension.py
    Certifique-se de que o serviço Python está rodando em localhost:8000

---

### Vantagens da Arquitetura
✅ Compatibilidade: Jython 2.7 só faz requisições HTTP simples

✅ Modernidade: Python 3.12 + OpenAI SDK completo no serviço

✅ Separação de responsabilidades: Burp = UI, Python = Lógica

✅ Fácil manutenção: Atualize a SDK do OpenAI sem quebrar Burp

✅ Escalabilidade: Serviço pode ser containerizado ou hospedado remotamente

✅ Segurança: API Key fica apenas no serviço Python, nunca em Jython
info about this project
