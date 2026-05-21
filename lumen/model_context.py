"""Structured model context primitives.

The runtime should treat the prompt as a rendered artifact. These dataclasses
keep section boundaries and metadata available before text is serialized for a
model provider.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ContextSection:
    raw: str
    budget: int | None = None
    rendered: str = ""
    name: str = ""
    details: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.raw = str(self.raw)
        if self.rendered == "":
            self.rendered = self.raw
        if self.details is None:
            self.details = {}

    @property
    def raw_chars(self):
        return len(self.raw)

    @property
    def rendered_chars(self):
        return len(self.rendered)

    def to_metadata(self):
        return {
            "name": self.name,
            "raw_chars": self.raw_chars,
            "budget_chars": self.budget,
            "rendered_chars": self.rendered_chars,
            "details": dict(self.details or {}),
        }


@dataclass
class ModelContext:
    sections: dict[str, ContextSection]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        for name, section in self.sections.items():
            if not section.name:
                section.name = name

    @property
    def section_order(self):
        return list(self.sections)

    def render_prompt(self, section_order=None, separator="\n\n"):
        order = list(section_order or self.section_order)
        return separator.join(self.sections[name].rendered for name in order if self.sections[name].rendered).strip()

    def section_metadata(self):
        return {
            name: section.to_metadata()
            for name, section in self.sections.items()
        }
