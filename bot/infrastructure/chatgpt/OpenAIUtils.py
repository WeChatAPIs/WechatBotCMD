from __future__ import annotations

import datetime

# from plugin_manager import PluginManager
import tiktoken

# Models can be found here: https://platform.openai.com/docs/models/overview
GPT_3_MODELS = ("gpt-3.5-turbo", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613")
GPT_3_16K_MODELS = ("gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613")
GPT_4_MODELS = ("gpt-4", "gpt-4-0314", "gpt-4-0613")
GPT_4_32K_MODELS = ("gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-0613")
GPT_ALL_MODELS = GPT_3_MODELS + GPT_3_16K_MODELS + GPT_4_MODELS + GPT_4_32K_MODELS


def default_max_tokens(model: str) -> int:
    """
    Gets the default number of max tokens for the given model.
    :param model: The model name
    :return: The default number of max tokens
    """
    base = 1200
    if model in GPT_3_MODELS:
        return base
    elif model in GPT_4_MODELS:
        return base * 2
    elif model in GPT_3_16K_MODELS:
        return base * 4
    elif model in GPT_4_32K_MODELS:
        return base * 8


def are_functions_available(model: str) -> bool:
    """
    Whether the given model supports functions
    """
    # Deprecated models
    if model in ("gpt-3.5-turbo-0301", "gpt-4-0314", "gpt-4-32k-0314"):
        return False
    # Stable models will be updated to support functions on June 27, 2023
    if model in ("gpt-3.5-turbo", "gpt-4", "gpt-4-32k"):
        return datetime.date.today() > datetime.date(2023, 6, 27)
    return True


def localized_text(key, data=None):
    """
    返回指定bot_language中键的已翻译文本。
    可以在 translations.json 中找到密钥和翻译。
    Return translated text for a key in specified bot_language.
    Keys and translations can be found in the translations.json.
    """
    return ""


def max_model_tokens(model: str) -> int:
    base = 4096
    if model in GPT_3_MODELS:
        return base
    if model in GPT_3_16K_MODELS:
        return base * 4
    if model in GPT_4_MODELS:
        return base * 2
    if model in GPT_4_32K_MODELS:
        return base * 8
    raise NotImplementedError(
        f"Max tokens for model {model} is not implemented yet."
    )


def count_tokens(messages: list, model: str) -> int:
    """
    计算发送给定消息所需的令牌数。
    Counts the number of tokens required to send the given messages.
    :param messages: the messages to send
    :return: the number of tokens required
    https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
    """

    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("gpt-3.5-turbo")

    if model in GPT_3_MODELS + GPT_3_16K_MODELS:
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model in GPT_4_MODELS + GPT_4_32K_MODELS:
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            if value is None:
                continue
            try:
                encData = encoding.encode(value)
            except Exception as e:
                encData = 1
            num_tokens += len(encData)
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens
