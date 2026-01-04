# Application Workflow Diagram

```mermaid
flowchart TD
    A[Check New Emails via IMAP] --> B[Extract Content]
    C[Receive Telegram Message] --> B
    D[Receive API Request] --> B
    B --> E[Add Saved Prompt to Content]
    E --> F[Send to Selected LLM Yandex-GPT/DeepSeek/Grok]
    F --> G[Receive LLM Response]
    G --> H{Source Type}
    H -->|Email| I[Send Reply via SMTP]
    H -->|Telegram| J[Send Message via Bot API]
    H -->|API| K[Create Jira Issue with Response]
    I --> L[Save History to PostgreSQL]
    J --> L
    K --> L
    L --> M[Log to Elasticsearch for Kibana]
    N[Healthcheck Endpoint] --> O[Grafana Monitoring]