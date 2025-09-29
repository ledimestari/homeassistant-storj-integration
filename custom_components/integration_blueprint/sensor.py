"""Sensor platform for integration_blueprint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .entity import IntegrationBlueprintEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import BlueprintDataUpdateCoordinator
    from .data import IntegrationBlueprintConfigEntry


# Define all sensors here
ENTITY_DESCRIPTIONS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="integration_blueprint",
        name="Integration Sensor ASS",
        icon="mdi:format-quote-close",
    ),
    SensorEntityDescription(
        key="wallet",
        name="Wallet",
        icon="mdi:wallet",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: IntegrationBlueprintConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        IntegrationBlueprintSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class IntegrationBlueprintSensor(IntegrationBlueprintEntity, SensorEntity):
    """Integration Blueprint Sensor class."""

    def __init__(
        self,
        coordinator: BlueprintDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def unique_id(self) -> str:
        """Return a unique ID for this sensor."""
        # Combine the entry_id (integration instance) with the sensor key
        return f"{self.coordinator.config_entry.entry_id}_{self.entity_description.key}"

    @property
    def native_value(self) -> str | None:
        """Return the native value depending on the sensor type."""
        if self.entity_description.key == "integration_blueprint":
            return self.coordinator.data.get("diskSpace", {}).get("used")
        if self.entity_description.key == "wallet":
            return self.coordinator.data.get("wallet")
        return None
