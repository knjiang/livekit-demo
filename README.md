# LiveKit Voice AI Agent Demo

A simple voice AI agent using LiveKit Agents with OpenAI's realtime model and Braintrust telemetry.

## Setup

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Configure environment variables:**
   ```bash
   # Get LiveKit credentials
   lk app env -w
   
   # Then add your OpenAI API key to .env.local
   # Optionally add Braintrust credentials for telemetry
   ```

3. **Download model files:**
   ```bash
   uv run agent.py download-files
   ```

## Usage

### Run in terminal (console mode):
```bash
uv run agent.py console
```

### Run in development mode:
```bash
uv run agent.py dev
```

Then visit the [Agents Playground](https://cloud.livekit.io/projects/p_/agents) to interact with your agent.

### Run in production mode:
```bash
uv run agent.py start
```

## Features

- ✅ OpenAI realtime voice model (natural, expressive conversations)
- ✅ Noise cancellation for clear audio
- ✅ Braintrust OTEL telemetry (optional monitoring)
- ✅ Simple setup with minimal configuration

## Learn More

- [LiveKit Agents Documentation](https://docs.livekit.io/agents/start/voice-ai/)
- [OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime)

