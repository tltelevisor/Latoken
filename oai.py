from openai import OpenAI
from config import API_KEY, OPENAI_MODEL, URL_LATOKEN, URL_HACKATHON, URL_CULTURE, FILES_DIR
import os, logging

logging.basicConfig(level=logging.INFO, filename='latoken.log',
                    format='%(asctime)s %(levelname)s %(message)s')

client = OpenAI(api_key=API_KEY)


# Сборка текста запроса из последнего сообщения и предыдущих из текущей темы
def collect_mess(user_id, message):
    sys_prompt = f'Ответь на русском языке'
    messages = [{"role": "user", "content": message}]
    # if topic:
    #     pr_post = Topic.query.filter_by(id = topic)[0].post_id
    #     while pr_post:
    #         post = Post.query.filter_by(id = pr_post)[0]
    #         if post.user_id == 1:
    #             messages.insert(0, {"role": "assistant", "content": post.body})
    #         if post.user_id == user_id:
    #             messages.insert(0, {"role": "user", "content": post.body})
    #         pr_post = post.reply_id
    messages.insert(0, {"role": "system", "content": sys_prompt})
    return messages

def context():
    files = os.listdir(FILES_DIR)
    file_content = ''
    for ef in files:
        file_path = f'{FILES_DIR}/{ef}'
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file_content + '\n' + file.read()
    return file_content

def oai_context(user_id, messages):
    new_messages = []
    for idx, em in enumerate(messages):
        if idx == (len(messages) - 1):  # в последнее сообщение добавляем контекст
            new_mess = {"role": "user",
                        "content": f"Здесь контекст из файлов:\n{context()}\n\nПожалуйста, ответь на вопрос: {em['content']}"}
        else:
            new_mess = em
        new_messages.append(new_mess)
    response = client.chat.completions.create(
        messages=new_messages,
        model=OPENAI_MODEL
    )
    logging.info(
        f'user_id: {user_id}, prompt_tokens: {response.usage.prompt_tokens}, completion_tokens: {response.usage.completion_tokens}')
    return response.choices[0].message.content.strip()

def oai_fact(user_id):
    sys_prompt = f'Ответь на русском языке'
    messages = [{"role": "user",
                 "content": f"Здесь контекст:\n{context()}\n\nВыбери случайный факт о LATOKEN и расскажи о нем."}]
    messages.insert(0, {"role": "system", "content": sys_prompt})
    response = client.chat.completions.create(
        messages=messages,
        model=OPENAI_MODEL
    )
    logging.info(
        f'user_id: {user_id}, prompt_tokens: {response.usage.prompt_tokens}, completion_tokens: {response.usage.completion_tokens}')
    return response.choices[0].message.content.strip()

def oai_give_question(user_id):
    messages = [{"role": "system",
                 "content": f"Твоя задача - задать вопрос по контексту: \n{context()}\n\n. На русском языке."}]

    response = client.chat.completions.create(
        messages=messages,
        model=OPENAI_MODEL
    )
    logging.info(
        f'user_id: {user_id}, prompt_tokens: {response.usage.prompt_tokens}, completion_tokens: {response.usage.completion_tokens}')
    return response.choices[0].message.content.strip()

def oai_check_answer(user_id, question, answer):
    messages = [{"role": "system",
                 "content": f"Твоя задача - оценить в баллах от 1 до 5, насколько ответ {answer} соответствует вопросу {question} в контексте: \n{context()}\n\n."}]
    response = client.chat.completions.create(
        messages=messages,
        model=OPENAI_MODEL
    )
    logging.info(
        f'user_id: {user_id}, prompt_tokens: {response.usage.prompt_tokens}, completion_tokens: {response.usage.completion_tokens}')
    return response.choices[0].message.content.strip()


def oai_no_context(user_id, messages):
    response = client.chat.completions.create(
        messages=messages,
        model=OPENAI_MODEL
    )
    logging.info(
        f'user_id: {user_id}, prompt_tokens: {response.usage.prompt_tokens}, completion_tokens: {response.usage.completion_tokens}')
    return response.choices[0].message.content.strip()
