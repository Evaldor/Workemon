# Workemon

AI-powered agent that processes emails, Telegram messages, and API requests by integrating with LLMs (Yandex-GPT, DeepSeek, Grok) and responds accordingly. Supports logging to Kibana, healthchecks for Grafana, and stores history in PostgreSQL. Runs in Docker.

## Promt

Сгенерированный при помощи AI простейший AI-агент
     
    промт:

    напиши на python приложение которое проверяет новые письма почтовом ящике yandex, сообщения полученные через месенджер telegarm, запросы приходящие на API, выбирает сожержимое и добавив к сохраненному промту отправляет в нейросеть LLM yandex-gpt, deepseek, grock или любую другую. полученный ответ от нейросети отправляет обратно, как ответ на письмо, сообщение в телеграмм, или создает задачку через API jira и помещает ответ в её описание. приложение должно работать в docker контейнере. приложение должно реализовывать лоирование в kibana и healthcheck в графану. приложение должно созранять историю запросов и ответов в бд PostgeSQL

    API keys and endpoints are in environment variables or config files; saved prompt is a fixed string like 'Process this request:'

    Provide specific examples: Yandex IMAP server, Telegram bot token, REST API endpoint, LLM API keys, Jira base URL; saved prompt is configurable

    No specific credentials yet, use placeholders; saved prompt is hard-coded in code

## Features

- **Email Processing**: Checks Yandex mailbox for new emails via IMAP, processes content with LLM, and sends replies via SMTP.
- **Telegram Bot**: Receives messages, processes with LLM, and replies.
- **REST API**: Accepts POST requests with content, returns LLM-processed responses.
- **LLM Integration**: Configurable support for Yandex-GPT, DeepSeek, or Grok.
- **Jira Integration**: Creates tasks in Jira with LLM responses.
- **Logging**: Structured logging with structlog, sent to Elasticsearch for Kibana visualization.
- **Monitoring**: Healthcheck endpoint at /health and Prometheus metrics at /metrics for Grafana.
- **Database**: Stores request-response history in PostgreSQL.
- **Dockerized**: Full container setup with docker-compose.

## Architecture

See `workflow_diagram.md` and `architecture_diagram.md` for details.

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd workemon
   ```

2. **Create .env file** with your credentials:
   ```
   DATABASE_URL=postgresql://user:password@postgres/workemon_db
   ELASTICSEARCH_URL=http://elasticsearch:9200
   LLM_PROVIDER=yandex
   SAVED_PROMPT=Process this request:
   YANDEX_IMAP_SERVER=imap.yandex.com
   YANDEX_USERNAME=your@yandex.com
   YANDEX_PASSWORD=yourpassword
   TELEGRAM_BOT_TOKEN=your_bot_token
   YANDEX_GPT_API_KEY=your_api_key
   DEEPSEEK_API_KEY=your_api_key
   GROK_API_KEY=your_api_key
   JIRA_URL=https://your-jira.atlassian.net
   JIRA_USERNAME=your@jira.com
   JIRA_PASSWORD=your_token
   JIRA_PROJECT_KEY=PROJ
   ```

3. **Run with Docker**:
   ```bash
   cd docker
   docker-compose up --build
   ```

   The app will be available at http://localhost:8000.

## Usage

- **API Endpoint**: POST to /process with JSON {"content": "your text"} to get LLM response.
- **Telegram**: Send message to the bot.
- **Email**: Send email to the configured Yandex account.
- **Healthcheck**: GET /health
- **Metrics**: GET /metrics

## Development

- Install dependencies: `pip install -r requirements.txt`
- Run tests: `python -m unittest discover tests`
- Run app: `uvicorn app.api_handler:app --reload`

## Notes

- Ensure API keys and credentials are set securely.
- For production, adjust Docker configs and add proper secrets management.
     