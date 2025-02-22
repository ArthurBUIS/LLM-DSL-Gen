# -*- coding: utf-8 -*-
# dsl_gen/agents/api.py

from ..config import API
from langchain_openai import ChatOpenAI

import logging

logger = logging.getLogger('dsl_gen')


def getClient(backend, temperature) -> ChatOpenAI:

    cfg = {
        'openai': API.MODEL_CFG.OpenAI,
        'ollama': API.MODEL_CFG.Ollama,
        'deepseek': API.MODEL_CFG.DeepSeek,
    }[backend]

    logger.info("Model loaded: %s, base_url: %s", cfg.model, cfg.base_url)

    return ChatOpenAI(
        model=cfg.model,
        openai_api_base=cfg.base_url,
        openai_api_key=cfg.api_key,
        temperature=temperature
    )
