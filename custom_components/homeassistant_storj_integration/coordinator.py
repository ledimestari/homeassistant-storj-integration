"""DataUpdateCoordinator for integration_blueprint."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from datetime import timedelta  # 🔹 import timedelta

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    IntegrationBlueprintApiClientAuthenticationError,
    IntegrationBlueprintApiClientError,
)

if TYPE_CHECKING:
    from .data import IntegrationBlueprintConfigEntry


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class BlueprintDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: IntegrationBlueprintConfigEntry

    def __init__(self, hass, config_entry: "IntegrationBlueprintConfigEntry") -> None:
        """Initialize coordinator with 10-minute update interval."""
        super().__init__(
            hass,
            _LOGGER=None,  # or pass a logger if you have one
            name="homeassistant_storj_integration",
            update_interval=timedelta(minutes=10),  # a 10-minute interval
        )
        self.config_entry = config_entry

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            client = self.config_entry.runtime_data.client

            sno_data = await client.async_get_data("/api/sno/")
            satellites_data = await client.async_get_data("/api/sno/satellites")
            estimated_payout_data = await client.async_get_data(
                "/api/sno/estimated-payout"
            )

            return {  # noqa: TRY300
                "sno": sno_data,
                "satellites": satellites_data,
                "estimated-payout": estimated_payout_data,
            }

        except IntegrationBlueprintApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except IntegrationBlueprintApiClientError as exception:
            raise UpdateFailed(exception) from exception
