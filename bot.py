import argparse
import asyncio
import os
import sys

import httpx
from dotenv import load_dotenv
from loguru import logger

from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.frames.frames import LLMRunFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import (
    LLMContextAggregatorPair,
    LLMUserAggregatorParams,
)
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.services.smallest.stt import SmallestSTTService
from pipecat.services.smallest.tts import SmallestTTSService
from pipecat.transports.daily.transport import DailyParams, DailyTransport

load_dotenv(override=True)

logger.remove(0)
logger.add(sys.stderr, level="INFO")


async def create_daily_room() -> tuple[str, str]:
    """Create a temporary Daily room and return (room_url, bot_token)."""
    api_key = os.getenv("DAILY_API_KEY")
    if not api_key:
        raise ValueError("DAILY_API_KEY is not set in your .env file.")

    async with httpx.AsyncClient() as client:
        room_resp = await client.post(
            "https://api.daily.co/v1/rooms",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"properties": {"max_participants": 2}},
        )
        room_resp.raise_for_status()
        room = room_resp.json()

        token_resp = await client.post(
            "https://api.daily.co/v1/meeting-tokens",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"properties": {"room_name": room["name"], "is_owner": True}},
        )
        token_resp.raise_for_status()
        token = token_resp.json()["token"]

    return room["url"], token


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smallest AI x Pipecat Voice Demo")
    parser.add_argument(
        "--voice",
        default="sophia",
        help="TTS voice ID to use (default: sophia)",
    )
    parser.add_argument(
        "--language",
        default="en",
        help="Language code for both STT and TTS (default: en). Examples: hi, de, fr, es, ta",
    )
    return parser.parse_args()


async def main():
    args = parse_args()
    room_url, token = await create_daily_room()

    print("\n" + "=" * 60)
    print("  Smallest AI x Pipecat — Voice Demo")
    print("=" * 60)
    print(f"\n  Join URL:\n\n    {room_url}\n")
    print(f"  Voice    : {args.voice}")
    print(f"  Language : {args.language}")
    print()
    print("  Open the URL above in your browser to talk to the bot.")
    print("  The bot uses Smallest AI for both STT and TTS.")
    print("\n  Press Ctrl+C to stop.\n")
    print("=" * 60 + "\n")

    transport = DailyTransport(
        room_url,
        token,
        "Smallest AI Bot",
        DailyParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
        ),
    )

    stt = SmallestSTTService(
        api_key=os.getenv("SMALLEST_API_KEY"),
        settings=SmallestSTTService.Settings(language=args.language),
    )

    tts = SmallestTTSService(
        api_key=os.getenv("SMALLEST_API_KEY"),
        sample_rate=24000,
        settings=SmallestTTSService.Settings(
            voice=args.voice,
            language=args.language,
        ),
    )

    llm = OpenAILLMService(
        api_key=os.getenv("OPENAI_API_KEY"),
        settings=OpenAILLMService.Settings(
            system_instruction=(
                "You are a helpful voice assistant powered by Smallest AI. "
                "Your responses will be spoken aloud, so keep them concise and conversational. "
                "Avoid emojis, markdown, bullet points, or any formatting that doesn't work in speech."
            ),
        ),
    )

    context = LLMContext()
    user_aggregator, assistant_aggregator = LLMContextAggregatorPair(
        context,
        user_params=LLMUserAggregatorParams(vad_analyzer=SileroVADAnalyzer()),
    )

    pipeline = Pipeline(
        [
            transport.input(),
            stt,
            user_aggregator,
            llm,
            tts,
            transport.output(),
            assistant_aggregator,
        ]
    )

    task = PipelineTask(
        pipeline,
        params=PipelineParams(
            enable_metrics=True,
            enable_usage_metrics=True,
        ),
    )

    @transport.event_handler("on_client_connected")
    async def on_client_connected(transport, client):
        logger.info("Client connected — starting conversation")
        context.add_message(
            {"role": "user", "content": "Greet the user warmly and let them know they can start talking."}
        )
        await task.queue_frames([LLMRunFrame()])

    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, client):
        logger.info("Client disconnected")
        await task.cancel()

    runner = PipelineRunner()
    await runner.run(task)


if __name__ == "__main__":
    asyncio.run(main())
