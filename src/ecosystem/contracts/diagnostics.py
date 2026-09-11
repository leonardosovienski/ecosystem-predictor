"""Native diagnostic payloads preserve domain-owned vocabularies.

These labels are observations in the producer's namespace, not members of a
universal scientific enum. No diagnostic grants permission to execute.
"""

from pydantic import BaseModel, ConfigDict, Field

from ecosystem.contracts.v1 import CapitalPermission


class NativeCapabilities(BaseModel):
    model_config = ConfigDict(extra="forbid")

    domain: str = Field(min_length=1)
    supports_prediction: bool
    supports_settlement: bool
    supports_collection: bool
    supports_no_opportunity: bool = True
    scientific_status: str = Field(min_length=1, strict=True)
    predictive_status: str = Field(min_length=1, strict=True)
    economic_status: str = Field(min_length=1, strict=True)
    capital_permission: CapitalPermission
    extra: dict = Field(default_factory=dict)
