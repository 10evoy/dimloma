import streamlit as st
import json
import pandas as pd
from task_selector import TaskSelector, TOPICS

# Настройка страницы
st.set_page_config(
    page_title="Индивидуальные траектории обучения теории вероятностей",
    page_icon="📊",
    layout="wide"
)

# Заголовок
st.title("Индивидуальные траектории обучения теории вероятностей")
st.markdown("""
Этот инструмент помогает создавать индивидуальные траектории обучения 
для школьников 7-9 классов по теории вероятностей с использованием ИИ.
""")

# Инициализация селектора задач
@st.cache_resource
def get_task_selector():
    return TaskSelector()

task_selector = get_task_selector()

# Создание боковой панели для ввода данных
with st.sidebar:
    st.header("Данные ученика")
    
    # Выбор текущей темы
    current_topic = st.selectbox(
        "Выберите текущую тему",
        options=TOPICS
    )
    
    # Количество задач
    num_tasks = st.slider(
        "Количество задач",
        min_value=1,
        max_value=10,
        value=5
    )
    
    # Кнопка для генерации задач
    generate_button = st.button("Сгенерировать задачи", type="primary")

# Основная часть - ввод оценок
st.header("Оценки ученика")

# Создание таблицы для ввода оценок
marks_data = {}
possible_marks = ["ещё не изучал", "2", "3", "4", "5"]

# Разделение тем на колонки для компактности
col1, col2 = st.columns(2)

for i, topic in enumerate(TOPICS):
    # Определение колонки
    col = col1 if i < len(TOPICS) // 2 else col2
    
    # Создание селектбокса для каждой темы
    with col:
        mark = st.selectbox(
            f"{topic}",
            options=possible_marks,
            key=f"mark_{i}"
        )
        
        # Преобразование строковой оценки в число, если это возможно
        if mark in ["2", "3", "4", "5"]:
            marks_data[topic] = int(mark)
        else:
            marks_data[topic] = mark

# Отображение задач
if generate_button:
    st.header("Сгенерированные задачи")
    
    # Создание данных ученика
    student_data = task_selector.create_student_data(current_topic, marks_data)
    
    # Получение задач
    with st.spinner("Генерация задач..."):
        tasks = task_selector.get_tasks_for_student(student_data, num_tasks=num_tasks)
    
    if tasks:
        # Отображение задач
        for i, task in enumerate(tasks, 1):
            with st.expander(f"Задача {i}: {task['условие'][:100]}...", expanded=True):
                st.markdown(f"**Условие:** {task['условие']}")
                st.markdown(f"**Тема:** {task['тема']}")
                st.markdown(f"**Сложность:** {task['сложность']}")
                st.markdown(f"**Тип:** {task['тип']}")
                
                # Кнопка для отображения ответа
                if st.button(f"Показать ответ к задаче {i}", key=f"answer_{i}"):
                    st.markdown(f"**Ответ:** {task['ответ']}")
    else:
        st.error("Не удалось сгенерировать задачи. Пожалуйста, попробуйте еще раз.")

# Информация о проекте
st.markdown("---")
st.markdown("""
### О проекте
Этот инструмент разработан в рамках магистерской работы по теме 
"Методика построения и реализации индивидуальных траекторий обучения школьников 7-9 классов 
теории вероятностей с использованием технологий искусственного интеллекта".

Инструмент использует:
- Данные об успеваемости ученика
- Искусственный интеллект для определения оптимальных задач
- Базу из 1200 задач по теории вероятностей
""")