from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import openai, noise_cancellation
from livekit.agents.telemetry import set_tracer_provider
from opentelemetry.sdk.trace import TracerProvider
from braintrust.otel import BraintrustSpanProcessor

def setup_braintrust_telemetry():
    """Setup Braintrust OTEL telemetry for agent monitoring"""
    trace_provider = TracerProvider()
    trace_provider.add_span_processor(BraintrustSpanProcessor())
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

    # Generate reply
    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )

    # Close the session via ctrl + c


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))

