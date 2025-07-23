from typing import Sequence
from autogen_agentchat.base import TerminationCondition, TerminatedException
from autogen_agentchat.messages import BaseAgentEvent, BaseChatMessage, StopMessage
from autogen_core import Component
from pydantic import BaseModel
from typing_extensions import Self

class FinalSummaryTerminationConfig(BaseModel):
    """Config for FinalSummaryTermination for serialization compatibility."""
    keyword: str = "✅ Final Structured Summary"

class FinalSummaryTermination(TerminationCondition, Component[FinalSummaryTerminationConfig]):
    """Terminates the chat when a specific keyword is found in the message content."""

    component_config_schema = FinalSummaryTerminationConfig
    component_provider_override = "custom.conditions.FinalSummaryTermination"

    def __init__(self, keyword: str = "✅ Final Structured Summary") -> None:
        self._terminated = False
        self._keyword = keyword

    @property
    def terminated(self) -> bool:
        return self._terminated

    async def __call__(self, messages: Sequence[BaseAgentEvent | BaseChatMessage]) -> StopMessage | None:
        if self._terminated:
            raise TerminatedException("Termination condition already met.")

        for message in messages:
            if isinstance(message, BaseChatMessage) and self._keyword in message.content:
                self._terminated = True
                return StopMessage(
                    content=f"Termination triggered by keyword: '{self._keyword}'",
                    source="FinalSummaryTermination"
                )
        return None

    async def reset(self) -> None:
        self._terminated = False

    def _to_config(self) -> FinalSummaryTerminationConfig:
        return FinalSummaryTerminationConfig(keyword=self._keyword)

    @classmethod
    def _from_config(cls, config: FinalSummaryTerminationConfig) -> Self:
        return cls(keyword=config.keyword)
