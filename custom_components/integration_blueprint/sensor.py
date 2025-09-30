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
        key="storj_diskspace_available",
        name="Diskspace Total",
        native_unit_of_measurement="GB",
        icon="mdi:harddisk",
    ),
    SensorEntityDescription(
        key="storj_diskspace_used",
        name="Diskspace Used",
        native_unit_of_measurement="GB",
        icon="mdi:harddisk",
    ),
    SensorEntityDescription(
        key="storj_diskspace_trash",
        name="Diskspace Trash",
        native_unit_of_measurement="GB",
        icon="mdi:harddisk",
    ),
    SensorEntityDescription(
        key="storj_diskspace_free",
        name="Diskspace Free",
        native_unit_of_measurement="GB",
        icon="mdi:harddisk",
    ),
    SensorEntityDescription(
        key="storj_average_usage_bytes",
        name="Average Disk Space Used This Month",
        native_unit_of_measurement="GB",
        icon="mdi:harddisk",
    ),
    SensorEntityDescription(
        key="storj_disk_use_percentage",
        name="Disk Use Percentage",
        native_unit_of_measurement="%",
        icon="mdi:harddisk",
    ),
    SensorEntityDescription(
        key="storj_nodeid",
        name="Node ID",
        icon="mdi:eye",
    ),
    SensorEntityDescription(
        key="storj_wallet",
        name="Wallet",
        icon="mdi:wallet",
    ),
    SensorEntityDescription(
        key="storj_quic",
        name="QUIC",
        icon="mdi:eye",
    ),
    SensorEntityDescription(
        key="storj_uptime",
        name="Uptime",
        icon="mdi:eye",
    ),
    SensorEntityDescription(
        key="storj_version",
        name="Version",
        icon="mdi:eye",
    ),
    SensorEntityDescription(
        key="storj_bandwidth_used",
        name="Bandwidth used this month",
        native_unit_of_measurement="GB",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="storj_bandwidth_egress",
        name="Bandwidth Egress this month",
        native_unit_of_measurement="GB",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="storj_bandwidth_ingress",
        name="Bandwidth Ingress this month",
        native_unit_of_measurement="GB",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="storj_current_month_payout",
        name="Estimated earning this month",
        native_unit_of_measurement="$",
        icon="mdi:currency-usd",
    ),
    SensorEntityDescription(
        key="storj_current_month_held",
        name="Held back this month",
        native_unit_of_measurement="$",
        icon="mdi:currency-usd",
    ),
    SensorEntityDescription(
        key="storj_current_month_pay_total",
        name="Gross total this month",
        native_unit_of_measurement="$",
        icon="mdi:currency-usd",
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
        disk_available = (
            self.coordinator.data["sno"].get("diskSpace", {}).get("available")
        )
        disk_used = self.coordinator.data["sno"].get("diskSpace", {}).get("used")
        disk_trash = self.coordinator.data["sno"].get("diskSpace", {}).get("trash")
        payout = (
            self.coordinator.data["estimated-payout"]
            .get("currentMonth", {})
            .get("payout")
        )
        held = (
            self.coordinator.data["estimated-payout"]
            .get("currentMonth", {})
            .get("held")
        )
        # ---
        if self.entity_description.key == "storj_diskspace_available":
            return round(float(disk_available / 1000000000), 2)
        # ---
        if self.entity_description.key == "storj_diskspace_used":
            return round(float(disk_used / 1000000000), 2)
        # ---
        if self.entity_description.key == "storj_diskspace_trash":
            return round(float(disk_trash / 1000000000), 2)
        # ---
        if self.entity_description.key == "storj_diskspace_free":
            disk_free = disk_available - disk_used - disk_trash
            return round(float(disk_free / 1000000000), 2)
        # ---
        if self.entity_description.key == "storj_average_usage_bytes":
            average_usage_bytes_raw = self.coordinator.data["satellites"].get(
                "averageUsageBytes"
            )
            if average_usage_bytes_raw is not None:
                average_usage_bytes_gb = average_usage_bytes_raw / 1000000000
                return round(float(average_usage_bytes_gb), 2)
        # ---
        if self.entity_description.key == "storj_disk_use_percentage":
            disk_used_percent = ((disk_used + disk_trash) / disk_available) * 100
            return round(float(disk_used_percent), 2)
        # ---
        if self.entity_description.key == "storj_wallet":
            return self.coordinator.data["sno"].get("wallet")
        # ---
        if self.entity_description.key == "storj_quic":
            return self.coordinator.data["sno"].get("quicStatus")
        # ---
        if self.entity_description.key == "storj_uptime":
            started_at_str = self.coordinator.data["sno"].get("startedAt")
            started_at = datetime.fromisoformat(started_at_str.replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            uptime = now - started_at
            days = uptime.days
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            return f"{days}d {hours}h {minutes}m"
        # ---
        if self.entity_description.key == "storj_version":
            return self.coordinator.data["sno"].get("version")
        # ---
        if self.entity_description.key == "storj_bandwidth_used":
            bandwidth_used_raw = (
                self.coordinator.data["sno"].get("bandwidth", {}).get("used")
            )
            if bandwidth_used_raw is not None:
                bandwidth_used_gb = bandwidth_used_raw / 1000000000
                return round(float(bandwidth_used_gb), 2)
        # ---
        if self.entity_description.key == "storj_bandwidth_egress":
            bandwidth_used_raw = self.coordinator.data["satellites"].get(
                "egressSummary"
            )
            if bandwidth_used_raw is not None:
                bandwidth_used_gb = bandwidth_used_raw / 1000000000
                return round(float(bandwidth_used_gb), 2)
        # ---
        if self.entity_description.key == "storj_bandwidth_ingress":
            bandwidth_used_raw = self.coordinator.data["satellites"].get(
                "ingressSummary"
            )
            if bandwidth_used_raw is not None:
                bandwidth_used_gb = bandwidth_used_raw / 1000000000
                return round(float(bandwidth_used_gb), 2)
        # ---
        if self.entity_description.key == "storj_nodeid":
            return self.coordinator.data["sno"].get("nodeID")
        # ---
        if self.entity_description.key == "storj_current_month_payout":
            return round(float(payout), 2)
        # ---
        if self.entity_description.key == "storj_current_month_held":
            return round(float(held), 2)
        # ---
        if self.entity_description.key == "storj_current_month_pay_total":
            pay_total = payout + held
            return round(float(pay_total), 2)
        return None
