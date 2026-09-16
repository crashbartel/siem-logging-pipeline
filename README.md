# The SIEM & Logging Pipeline

An educational, Docker-based security monitoring lab that generates synthetic authentication events, collects them with Grafana Alloy, stores them in Grafana Loki, and visualizes detection results in Grafana.

The project demonstrates an end-to-end logging pipeline and a simple brute-force detection use case without requiring access to real authentication data.

## Architecture

```text
Python generator -> shared JSONL log -> Grafana Alloy -> Grafana Loki -> Grafana
```

| Component | Purpose |
| --- | --- |
| Python generator | Produces normal and simulated brute-force authentication events |
| Grafana Alloy `v1.0.0` | Tails the shared log file and forwards entries to Loki |
| Grafana Loki `3.1.0` | Stores and queries log data |
| Grafana `11.4.0` | Displays the provisioned SIEM dashboard |

## What the lab demonstrates

- Docker Compose service orchestration and networking
- Structured JSON security-event generation
- File-based log collection with Grafana Alloy
- Log storage and LogQL queries with Loki
- Automatically provisioned Grafana data source and dashboard
- Brute-force detection based on repeated authentication failures
- Normal and attack-simulation test modes

Each generated event contains a timestamp, unique event ID, username, RFC 5737 documentation IP address, authentication outcome, event type, and scenario label.

## Prerequisites

- Docker Desktop with Docker Compose
- Git
- PowerShell

## Quick start

Run these commands from the repository root.

1. Create a local `.env` file containing a Grafana administrator password. Save the file as UTF-8, not UTF-16.

   ```text
   GRAFANA_ADMIN_PASSWORD=replace-with-a-strong-local-password
   ```

   The `.env` file is ignored by Git and must not be committed.

2. Build and start the lab.

   ```powershell
   docker compose --env-file .env up -d --build
   docker compose --env-file .env ps -a
   ```

3. Wait approximately 15 seconds for Loki to become ready, then verify the services.

   ```powershell
   Invoke-RestMethod "http://localhost:9090/ready" -TimeoutSec 10
   Invoke-RestMethod "http://localhost:3001/api/health" -TimeoutSec 10 | ConvertTo-Json
   ```

4. Open [Grafana](http://localhost:3001), sign in as `admin` using the password in `.env`, and open **The SIEM & Logging Pipeline** dashboard.

## Generate test data

Generate five normal authentication events:

```powershell
docker compose --env-file .env run --rm generator `
  python /app/scripts/generator.py --mode normal
```

Generate a simulated brute-force scenario:

```powershell
docker compose --env-file .env run --rm generator `
  python /app/scripts/generator.py --mode brute-force
```

The generator is a one-shot container. An `Exited (0)` status after it finishes is expected and indicates success.

## Dashboard

The provisioned dashboard contains 11 panels:

1. Total Authentication Events
2. Successful Authentications
3. Failed Authentications
4. Successes and Failures Over Time
5. Top Source IPs Producing Failures
6. Raw Authentication Logs
7. Failed Logins by Source IP
8. Failed Logins by Username
9. Possible Brute-Force Sources
10. Authentication Events by Scenario
11. Raw Security Events

The **Possible Brute-Force Sources** panel identifies a source IP that produces at least five failed authentication events within a five-minute window. The included attack simulation generates enough failures from one documentation IP to trigger this detection.

## Project structure

```text
.
|-- alloy/
|   `-- config.alloy
|-- grafana/
|   `-- provisioning/
|       |-- dashboards/
|       |   |-- dashboard-provisioning.yaml
|       |   `-- siem-dashboard.json
|       `-- datasources/
|           `-- datasource.yml
|-- loki/
|   `-- config.yml
|-- scripts/
|   `-- generator.py
|-- .gitignore
|-- Dockerfile
|-- docker-compose.yml
`-- README.md
```

Runtime data, logs, credentials, and local service state are excluded through `.gitignore`.

## Useful operations

View container status:

```powershell
docker compose --env-file .env ps -a
```

Inspect service logs:

```powershell
docker logs --tail 100 siem-generator
docker logs --tail 100 siem-alloy
docker logs --tail 100 siem-loki
docker logs --tail 100 siem-grafana
```

Stop the lab while preserving local data:

```powershell
docker compose --env-file .env down
```

## Troubleshooting

- **Loki initially reports that the ingester is not ready:** wait 15 seconds and retry the readiness request.
- **Grafana cannot reach Loki:** confirm both containers are attached to the same Compose network and that the provisioned URL is `http://loki:3100`.
- **No recent dashboard data:** select a wider time range, run the generator again, and refresh the dashboard.
- **Compose reports invalid characters in `.env`:** recreate the file as UTF-8 without a byte-order mark.
- **Generator shows `Exited (0)`:** this is normal because the generator finishes after writing its test events.

## Security and scope

This repository is an educational home lab, not a production SIEM. It uses synthetic data and local filesystem storage. It does not implement production-grade authentication, TLS, high availability, secrets management, alert routing, backups, or retention policies. Keep all ports bound to localhost unless you intentionally add appropriate network protections.

## Resume talking points

- Built a four-service, containerized log pipeline using Python, Grafana Alloy, Loki, and Grafana.
- Created structured authentication telemetry and repeatable normal/brute-force simulations.
- Implemented LogQL-based analysis and a provisioned 11-panel dashboard for security monitoring.
- Diagnosed container mounts, service networking, configuration syntax, and end-to-end ingestion failures.
