# ai_service/main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import openai
import os
from pathlib import Path

app = FastAPI(title="ChatGPT AI Service", version="1.0.0")

openai.api_key = os.getenv("OPENAI_API_KEY")

class PromptRequest(BaseModel):
    prompt: str
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 500

class PromptResponse(BaseModel):
    response: str
    usage: dict

# ============ ROOT & HEALTH ENDPOINTS ============

@app.get("/", response_class=HTMLResponse)
async def root():
    """Endpoint raiz - Retorna interface HTML"""
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ChatGPT AI Service - Burp Integration</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            
            .container {
                background: white;
                border-radius: 12px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                max-width: 600px;
                width: 100%;
                padding: 40px;
            }
            
            h1 {
                color: #333;
                margin-bottom: 10px;
                font-size: 28px;
            }
            
            .status {
                display: inline-block;
                background: #10b981;
                color: white;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
                margin-bottom: 20px;
            }
            
            .section {
                margin-bottom: 30px;
                padding-bottom: 30px;
                border-bottom: 1px solid #e5e7eb;
            }
            
            .section:last-child {
                border-bottom: none;
            }
            
            h2 {
                color: #667eea;
                font-size: 16px;
                margin-bottom: 12px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .endpoint {
                background: #f3f4f6;
                padding: 12px;
                border-radius: 6px;
                margin-bottom: 12px;
                font-family: 'Courier New', monospace;
                font-size: 13px;
                border-left: 4px solid #667eea;
            }
            
            .method {
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 2px 8px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
                margin-right: 8px;
            }
            
            .method.get { background: #10b981; }
            .method.post { background: #f59e0b; }
            .method.health { background: #06b6d4; }
            
            textarea {
                width: 100%;
                padding: 12px;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                font-family: 'Courier New', monospace;
                font-size: 13px;
                resize: vertical;
                min-height: 100px;
                margin-bottom: 10px;
            }
            
            button {
                background: #667eea;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-weight: bold;
                transition: background 0.3s;
            }
            
            button:hover {
                background: #764ba2;
            }
            
            button:active {
                transform: scale(0.98);
            }
            
            .response {
                background: #f3f4f6;
                padding: 12px;
                border-radius: 6px;
                margin-top: 10px;
                max-height: 200px;
                overflow-y: auto;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                white-space: pre-wrap;
                word-break: break-word;
                display: none;
            }
            
            .response.show {
                display: block;
            }
            
            .response.success {
                border-left: 4px solid #10b981;
                color: #059669;
            }
            
            .response.error {
                border-left: 4px solid #ef4444;
                color: #dc2626;
            }
            
            .input-group {
                margin-bottom: 12px;
            }
            
            label {
                display: block;
                font-weight: bold;
                color: #333;
                margin-bottom: 6px;
                font-size: 13px;
            }
            
            input[type="text"], input[type="number"] {
                width: 100%;
                padding: 8px 12px;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                font-size: 13px;
                margin-bottom: 10px;
            }
            
            .info-box {
                background: #dbeafe;
                border-left: 4px solid #3b82f6;
                padding: 12px;
                border-radius: 6px;
                font-size: 13px;
                color: #1e40af;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 ChatGPT AI Service</h1>
            <span class="status">✓ Online</span>
            
            <div class="info-box">
                <strong>Status:</strong> Servidor rodando com sucesso!<br>
                <strong>Endpoint API:</strong> http://127.0.0.1:8000/api/chat<br>
                <strong>Health Check:</strong> http://127.0.0.1:8000/health
            </div>
            
            <!-- SECTION: API ENDPOINTS -->
            <div class="section">
                <h2>📡 API Endpoints</h2>
                
                <div class="endpoint">
                    <span class="method get">GET</span><strong>/</strong>
                    <p style="margin-top: 6px; color: #666; font-size: 12px;">Interface web de teste (esta página)</p>
                </div>
                
                <div class="endpoint">
                    <span class="method health">GET</span><strong>/health</strong>
                    <p style="margin-top: 6px; color: #666; font-size: 12px;">Verificar status do serviço</p>
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span><strong>/docs</strong>
                    <p style="margin-top: 6px; color: #666; font-size: 12px;">Documentação interativa (Swagger UI)</p>
                </div>
                
                <div class="endpoint">
                    <span class="method post">POST</span><strong>/api/chat</strong>
                    <p style="margin-top: 6px; color: #666; font-size: 12px;">Enviar prompt para processamento com OpenAI</p>
                </div>
            </div>
            
            <!-- SECTION: TEST CHAT -->
            <div class="section">
                <h2>💬 Testar API</h2>
                
                <div class="input-group">
                    <label for="prompt">Prompt:</label>
                    <textarea id="prompt" placeholder="Digite seu prompt aqui...">Explique o que é uma variável em programação.</textarea>
                </div>
                
                <div class="input-group">
                    <label for="model">Modelo:</label>
                    <input type="text" id="model" value="gpt-3.5-turbo" placeholder="gpt-3.5-turbo">
                </div>
                
                <div class="input-group">
                    <label for="maxTokens">Max Tokens:</label>
                    <input type="number" id="maxTokens" value="500" min="1" max="4000">
                </div>
                
                <button onclick="sendRequest()">📤 Enviar Request</button>
                
                <div id="response" class="response">
                    <!-- Response will be shown here -->
                </div>
            </div>
            
            <!-- SECTION: INTEGRATION -->
            <div class="section">
                <h2>🔗 Integração com Burp Suite</h2>
                <p style="color: #666; font-size: 13px; line-height: 1.6; margin-bottom: 12px;">
                    A extensão Burp enviará requisições para este serviço. Certifique-se de:
                </p>
                <ul style="margin-left: 20px; color: #666; font-size: 13px; line-height: 1.8;">
                    <li>✓ Este servidor está rodando em http://127.0.0.1:8000</li>
                    <li>✓ A variável OPENAI_API_KEY está configurada</li>
                    <li>✓ O Burp consegue conectar neste endereço</li>
                    <li>✓ Sem firewall bloqueando a porta 8000</li>
                </ul>
            </div>
        </div>
        
        <script>
            async function sendRequest() {
                const prompt = document.getElementById('prompt').value;
                const model = document.getElementById('model').value;
                const maxTokens = parseInt(document.getElementById('maxTokens').value);
                const responseDiv = document.getElementById('response');
                
                if (!prompt.trim()) {
                    alert('Por favor, digite um prompt!');
                    return;
                }
                
                responseDiv.innerHTML = '⏳ Enviando...';
                responseDiv.classList.add('show');
                
                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            prompt: prompt,
                            model: model,
                            max_tokens: maxTokens
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        responseDiv.classList.remove('error');
                        responseDiv.classList.add('success');
                        responseDiv.innerHTML = `✓ Resposta:\n${data.response}\n\n📊 Uso:\n${JSON.stringify(data.usage, null, 2)}`;
                    } else {
                        responseDiv.classList.remove('success');
                        responseDiv.classList.add('error');
                        responseDiv.innerHTML = `✗ Erro: ${data.detail}`;
                    }
                } catch (error) {
                    responseDiv.classList.remove('success');
                    responseDiv.classList.add('error');
                    responseDiv.innerHTML = `✗ Erro de conexão: ${error.message}`;
                }
            }
            
            // Allow Enter key in textarea
            document.getElementById('prompt').addEventListener('keydown', function(e) {
                if (e.ctrlKey && e.key === 'Enter') {
                    sendRequest();
                }
            });
        </script>
    </body>
    </html>
    """

@app.get("/health")
async def health():
    """Health check endpoint - Verifica se o serviço está funcionando"""
    return {
        "status": "ok",
        "service": "ChatGPT AI Service",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/chat",
            "health": "/health",
            "docs": "/docs"
        }
    }

# ============ AI CHAT ENDPOINTS ============

@app.post("/api/chat", response_model=PromptResponse)
async def chat(request: PromptRequest):
    """
    Endpoint principal para chat com OpenAI.
    
    Recebe um prompt e retorna a resposta do modelo.
    Utilizado pela extensão Burp Suite.
    """
    if not openai.api_key:
        raise HTTPException(
            status_code=500, 
            detail="OPENAI_API_KEY não configurada no servidor"
        )
    
    try:
        response = openai.ChatCompletion.create(
            model=request.model,
            messages=[{"role": "user", "content": request.prompt}],
            max_tokens=request.max_tokens
        )
        return PromptResponse(
            response=response.choices[0].message.content,
            usage=response.usage.dict()
        )
    except openai.error.AuthenticationError:
        raise HTTPException(
            status_code=401, 
            detail="Erro de autenticação com OpenAI. Verifique sua API Key."
        )
    except openai.error.RateLimitError:
        raise HTTPException(
            status_code=429, 
            detail="Limite de requisições atingido. Tente novamente mais tarde."
        )
    except openai.OpenAIError as e:
        raise HTTPException(status_code=400, detail=f"Erro OpenAI: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# ============ INFO ENDPOINTS ============

@app.get("/api/models")
async def get_models():
    """Lista modelos disponíveis"""
    return {
        "available_models": [
            "gpt-3.5-turbo",
            "gpt-4",
            "gpt-4-turbo-preview"
        ],
        "default": "gpt-3.5-turbo"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8000,
        log_level="info"
    )
