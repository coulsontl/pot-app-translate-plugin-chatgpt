async function translate(text, from, to, options) {
    // 使用x.ai Grok的默认模型
    const DEFAULT_MODEL = "grok-2-1212";
    return translate_core(text, from, to, options, DEFAULT_MODEL);
} 