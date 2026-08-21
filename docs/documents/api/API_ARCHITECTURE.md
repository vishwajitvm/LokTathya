# API Architecture
LokTathya employs a strict Pydantic DTO (Data Transfer Object) boundary. SQLAlchemy database models are NEVER returned directly to the client to prevent credential/internal schema leakage.
