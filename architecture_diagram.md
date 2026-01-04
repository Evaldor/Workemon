# System Architecture Diagram

```mermaid
graph TB
    subgraph Docker Containers
        A[Python App FastAPI]
        B[PostgreSQL DB]
        C[Elasticsearch]
    end

    subgraph External Services
        D[Yandex Mail IMAP]
        E[Telegram Bot API]
        F[Incoming REST API Clients]
        G[LLM Services Yandex-GPT/DeepSeek/Grok]
        H[Jira API]
        I[Kibana]
        J[Grafana]
    end

    A --> B
    A --> C
    A --> D
    A --> E
    A --> F
    A --> G
    A --> H
    C --> I
    A --> J