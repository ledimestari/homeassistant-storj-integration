"""Adds config flow for Blueprint."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from slugify import slugify

from .api import (
    IntegrationBlueprintApiClient,
    IntegrationBlueprintApiClientCommunicationError,
    IntegrationBlueprintApiClientError,
)
from .const import DOMAIN, LOGGER


class BlueprintFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Blueprint."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        _errors: dict[str, str] = {}

        if user_input is not None:
            try:
                await self._test_connection(
                    host=user_input[CONF_HOST],
                    port=user_input[CONF_PORT],
                )
            except IntegrationBlueprintApiClientCommunicationError as exception:
                LOGGER.error("Connection error: %s", exception)
                _errors["base"] = "connection"
            except IntegrationBlueprintApiClientError as exception:
                LOGGER.exception("Unexpected error: %s", exception)
                _errors["base"] = "unknown"
            else:
                unique_id = f"{user_input[CONF_HOST]}:{int(user_input[CONF_PORT])}"
                await self.async_set_unique_id(slugify(unique_id))
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=unique_id,
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_HOST,
                        default=(user_input or {}).get(CONF_HOST, vol.UNDEFINED),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                    vol.Required(
                        CONF_PORT,
                        default=(user_input or {}).get(CONF_PORT, 14002),
                    ): selector.NumberSelector(
                        selector.NumberSelectorConfig(
                            min=1,
                            max=65535,
                            mode=selector.NumberSelectorMode.BOX,
                        ),
                    ),
                },
            ),
            errors=_errors,
        )

    async def _test_connection(self, host: str, port: int) -> None:
        """Validate that the device is reachable."""
        client = IntegrationBlueprintApiClient(
            host=host,
            port=port,
            session=async_create_clientsession(self.hass),
        )
        await client.async_get_data()
