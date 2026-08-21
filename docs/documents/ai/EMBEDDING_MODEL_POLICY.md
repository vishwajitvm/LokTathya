# Embedding Architecture & Model Policy
Models are registered in `ai_embedding_model` as PRIMARY, FALLBACK, or EXPERIMENTAL.
Structured numeric facts (like Budgets) are NOT embedded. We only embed narrative reports, policy docs, and notifications.
Vector spaces are never mixed.
