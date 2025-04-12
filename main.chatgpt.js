async function translate(text, from, to, options) {
    // 使用OpenAI的默认模型
    const DEFAULT_MODEL = "gpt-4o";
    return translate_core(text, from, to, options, DEFAULT_MODEL);
} 