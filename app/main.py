import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from datetime import datetime
import sys
from pathlib import Path
import time

# Добавляем родительскую директорию в путь
sys.path.append(str(Path(__file__).parent.parent))

from app.config import config
from app.database import DatabaseManager

class ChatApp:
    def __init__(self):
        # Инициализация базы данных с повторными попытками
        retry_count = 5
        for i in range(retry_count):
            try:
                self.db = DatabaseManager()
                break
            except Exception as e:
                if i == retry_count - 1:  # Если это последняя попытка
                    st.error(f"Не удалось подключиться к базе данных: {str(e)}")
                    raise e
                time.sleep(1)  # Ждем 1 секунду перед следующей попыткой

        self._init_session_state()
        self._init_page()
        
    def _init_session_state(self):
        """Инициализация состояния сессии"""
        if "api_key" not in st.session_state:
            st.session_state.api_key = None
            st.session_state.session_id = None
            st.session_state.chat_initialized = False
            st.session_state.messages = []

        # Генерация ID сессии, если его нет
        if not st.session_state.session_id:
            st.session_state.session_id = str(datetime.utcnow().timestamp())
            try:
                st.session_state.messages = self.db.load_chat_history(st.session_state.session_id)
            except Exception as e:
                st.error(f"Ошибка при загрузке истории чата: {str(e)}")
                st.session_state.messages = []

    def _init_page(self):
        """Инициализация страницы"""
        st.set_page_config(
            page_title="Llama-3 Chat",
            page_icon="🤖",
            layout="wide" if config.app.debug else "centered"
        )

    def _initialize_chat(self, api_key: str, messages: list) -> ConversationChain:
        """Инициализация чата с историей"""
        try:
            model = ChatOpenAI(
                api_key=api_key,
                base_url=config.api.base_url,
                model=config.api.model
            )
            # Инициализация памяти с существующей историей
            memory = ConversationBufferMemory()
            conversation = ConversationChain(llm=model, memory=memory)
            
            # Загрузка истории в память
            for msg in messages:
                if msg["role"] == "user":
                    memory.chat_memory.add_user_message(msg["content"])
                elif msg["role"] == "assistant":
                    memory.chat_memory.add_ai_message(msg["content"])
            
            return conversation
        except Exception as e:
            st.error(f"Ошибка инициализации чата: {str(e)}")
            return None

    def _show_debug_info(self):
        """Отображение отладочной информации"""
        if config.app.debug:
            with st.sidebar.expander("🔧 Debug Info"):
                st.write("Session ID:", st.session_state.session_id)
                st.write("Chat Initialized:", st.session_state.chat_initialized)
                st.write("Messages Count:", len(st.session_state.messages))

    def _show_sidebar(self):
        """Отображение боковой панели"""
        with st.sidebar:
            st.title("⚙️ Настройки")
            
            # Кнопка очистки истории
            if st.button("🗑️ Очистить историю"):
                self.db.clear_chat_history(st.session_state.session_id)
                st.session_state.messages = []
                st.session_state.chat_initialized = False
                st.rerun()

            # Debug информация
            self._show_debug_info()

    def _handle_api_key_input(self):
        """Обработка ввода API ключа"""
        st.title("🔑 Введите API ключ")
        api_key = st.text_input("OpenAI API ключ:", type="password")
        if st.button("Подтвердить"):
            if api_key:
                st.session_state.api_key = api_key
                st.success("✅ API ключ установлен!")
                st.rerun()
            else:
                st.error("❌ Пожалуйста, введите API ключ")

    def _handle_chat(self):
        """Обработка чата"""
        st.title("💬 Чат с Llama-3")
        
        # Инициализация чата при первом запуске или после очистки
        if not st.session_state.chat_initialized:
            conversation = self._initialize_chat(st.session_state.api_key, st.session_state.messages)
            if conversation:
                st.session_state.conversation = conversation
                st.session_state.chat_initialized = True
            else:
                st.session_state.api_key = None
                st.rerun()
        
        # Отображение истории сообщений
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Поле ввода сообщения
        if prompt := st.chat_input("Введите ваше сообщение..."):
            # Сохраняем и отображаем сообщение пользователя
            self.db.save_message(st.session_state.session_id, "user", prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            
            # Получаем и сохраняем ответ от модели
            with st.chat_message("assistant"):
                try:
                    response = st.session_state.conversation.predict(input=prompt)
                    st.write(response)
                    self.db.save_message(st.session_state.session_id, "assistant", response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Ошибка при генерации ответа: {str(e)}")

    def run(self):
        """Запуск приложения"""
        try:
            # Отображение боковой панели
            self._show_sidebar()
            
            # Основной интерфейс
            if not st.session_state.api_key:
                self._handle_api_key_input()
            else:
                self._handle_chat()

        except Exception as e:
            st.error(f"Критическая ошибка: {str(e)}")
            if config.app.debug:
                st.exception(e)

if __name__ == "__main__":
    app = ChatApp()
    app.run() 