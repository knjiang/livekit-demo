from dotenv import load_dotenv
import os

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import openai, noise_cancellation
from livekit.agents.telemetry import set_tracer_provider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

load_dotenv(".env.local")


def setup_braintrust_telemetry():
    """Setup Braintrust OTEL telemetry for agent monitoring"""
    api_key = os.getenv("BRAINTRUST_API_KEY")
    braintrust_parent = os.getenv("BRAINTRUST_PARENT")

    if not api_key or not braintrust_parent:
        print("Warning: Braintrust telemetry not configured. Set BRAINTRUST_API_KEY and BRAINTRUST_PARENT")
        return

    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "https://api.braintrust.dev/otel"
    os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = (
        f"Authorization=Bearer {api_key}, x-bt-parent={braintrust_parent}"
    )

    trace_provider = TracerProvider()
    trace_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    set_tracer_provider(trace_provider)
    print("✓ Braintrust telemetry enabled")


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful voice AI assistant.")


async def entrypoint(ctx: agents.JobContext):
    # Setup telemetry
    setup_braintrust_telemetry()

    # Create agent session with OpenAI realtime model
    session = AgentSession(
        llm=openai.realtime.RealtimeModel(voice="coral")
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))

