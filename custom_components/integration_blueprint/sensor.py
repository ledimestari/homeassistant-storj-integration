"""Sensor platform for integration_blueprint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .entity import IntegrationBlueprintEntity

from datetime import datetime, timezone

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import BlueprintDataUpdateCoordinator
    from .data import IntegrationBlueprintConfigEntry


# Define all sensors here
ENTITY_DESCRIPTIONS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="diskspace_available",
        name="Diskspace Total",
        native_unit_of_measurement="GB",
        icon="mdi:harddisk",
    ),
    SensorEntityDescription(
        key="diskspace_used",
        name="Diskspace Used",
        native_unit_of_measurement="GB",
        icon="mdi:harddisk",
    ),
    SensorEntityDescription(
        key="diskspace_trash",
        name="Diskspace Trash",
        native_unit_of_measurement="GB",
        icon="mdi:harddisk",
    ),
    SensorEntityDescription(
        key="diskspace_free",
        name="Diskspace Free",
        native_unit_of_measurement="GB",
        icon="mdi:harddisk",
    ),
    SensorEntityDescription(
        key="nodeid",
        name="Node ID",
        icon="mdi:eye",
    ),
    SensorEntityDescription(
        key="wallet",
        name="Wallet",
        icon="mdi:wallet",
    ),
    SensorEntityDescription(
        key="quic",
        name="QUIC",
        icon="mdi:eye",
    ),
    SensorEntityDescription(
        key="uptime",
        name="Uptime",
        icon="mdi:eye",
    ),
    SensorEntityDescription(
        key="version",
        name="Version",
        icon="mdi:eye",
    ),
    SensorEntityDescription(
        key="bandwidth_used",
        name="Bandwidth used this month",
        native_unit_of_measurement="GB",
        icon="mdi:chart-line",
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
        disk_available = self.coordinator.data.get("diskSpace", {}).get("available")
        disk_used = self.coordinator.data.get("diskSpace", {}).get("used")
        disk_trash = self.coordinator.data.get("diskSpace", {}).get("trash")

        if self.entity_description.key == "diskspace_available":
            return round(float(disk_available / 1000000000), 2)
        if self.entity_description.key == "diskspace_used":
            return round(float(disk_used / 1000000000), 2)
        if self.entity_description.key == "diskspace_trash":
            return round(float(disk_trash / 1000000000), 2)
        if self.entity_description.key == "diskspace_free":
            disk_free = disk_available - disk_used - disk_trash
            return round(float(disk_free / 1000000000), 2)
        if self.entity_description.key == "wallet":
            return self.coordinator.data.get("wallet")
        if self.entity_description.key == "quic":
            return self.coordinator.data.get("quicStatus")
        if self.entity_description.key == "uptime":
            started_at_str = self.coordinator.data.get("startedAt")
            started_at = datetime.fromisoformat(started_at_str.replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            uptime = now - started_at
            days = uptime.days
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            return f"{days}d {hours}h {minutes}m"
        if self.entity_description.key == "version":
            return self.coordinator.data.get("version")
        if self.entity_description.key == "bandwidth_used":
            bandwidth_used_raw = self.coordinator.data.get("bandwidth", {}).get("used")
            if bandwidth_used_raw is not None:
                bandwidth_used_gb = bandwidth_used_raw / 1000000000
                return round(float(bandwidth_used_gb), 2)
        if self.entity_description.key == "nodeid":
            return self.coordinator.data.get("nodeID")
        return None
