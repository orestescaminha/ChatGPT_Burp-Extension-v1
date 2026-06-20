# -*- coding: utf-8 -*-
# burp_extension.py
from burp import IBurpExtender, ITab, IContextMenuFactory
from java.io import PrintWriter
from javax.swing import JPanel, JButton, JTextArea, JScrollPane, BoxLayout, JLabel
from java.awt.event import ActionListener
import httplib
import json
import threading

class BurpExtender(IBurpExtender, ITab, IContextMenuFactory):
    
    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self.helpers = callbacks.getHelpers()
        self.stdout = PrintWriter(callbacks.getStdout(), True)
        self.stderr = PrintWriter(callbacks.getStderr(), True)
        
        callbacks.setExtensionName("ChatGPT Integration (HTTP Client)")
        callbacks.registerContextMenuFactory(self)
        self.init_ui(callbacks)
        
        self.ai_host = "127.0.0.1"
        self.ai_port = 8000
        self.stdout.println("[*] Extension loaded. AI Service should run on localhost:8000")
    
    def init_ui(self, callbacks):
        self.panel = JPanel()
        self.panel.setLayout(BoxLayout(self.panel, BoxLayout.Y_AXIS))
        
        label = JLabel("ChatGPT Integration - HTTP Client Mode")
        self.text_area = JTextArea(15, 60)
        self.text_area.setEditable(False)
        scroll = JScrollPane(self.text_area)
        
        self.panel.add(label)
        self.panel.add(scroll)
        
        callbacks.customizeUiComponent(self.panel)
        callbacks.addSuiteTab(self)
    
    def log_message(self, msg):
        self.text_area.append(msg + "\n")
        self.stdout.println("[ChatGPT] " + msg)
    
    def send_to_ai_service(self, prompt):
        """Envia requisição HTTP para o serviço Python 3"""
        try:
            conn = httplib.HTTPConnection(self.ai_host, self.ai_port, timeout=10)
            
            payload = json.dumps({
                "prompt": prompt,
                "model": "gpt-3.5-turbo",
                "max_tokens": 500
            })
            
            headers = {
                "Content-Type": "application/json",
                "Content-Length": str(len(payload))
            }
            
            conn.request("POST", "/api/chat", payload, headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
            
            if response.status == 200:
                result = json.loads(data)
                return result.get("response", "No response")
            else:
                return "Erro: " + str(response.status) + " - " + data
                
        except Exception as e:
            error_msg = "Erro ao conectar ao AI Service: " + str(e)
            self.log_message(error_msg)
            return error_msg
    
    def createMenuItems(self, invocation):
        menu_items = []
        menu_items.append(MenuItemHandler(self, invocation))
        return menu_items
    
    def getTabCaption(self):
        return "ChatGPT (HTTP Client)"
    
    def getUiComponent(self):
        return self.panel


class MenuItemHandler(ActionListener):
    def __init__(self, extender, invocation):
        self.extender = extender
        self.invocation = invocation
    
    def actionPerformed(self, event):
        selected_messages = self.invocation.getSelectedMessages()
        
        if selected_messages:
            message = selected_messages[0]
            request_text = self.extender.helpers.bytesToString(message.getRequest())
            
            self.extender.log_message("Enviando para AI Service...")
            response = self.extender.send_to_ai_service(request_text)
            self.extender.log_message("Resposta: " + response)
