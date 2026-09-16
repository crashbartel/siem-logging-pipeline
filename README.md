# SIEM Logging Pipeline

This project implements a complete SIEM logging pipeline that demonstrates real-time log analysis and threat detection using Docker and various open-source tools.

## Components

1. **Log Generator** (`scripts/generator.py`) - Generates synthetic authentication events
2. **Logstash** - Processes and parses logs for SIEM analysis
3. **Elasticsearch** - Stores and indexes log data
4. **Kibana** - Visualizes security analytics
5. **Grafana** - Provides dashboard monitoring and real-time alerting

## Quick Start

1. Build and start the system:
   ```
   docker-compose up -d
   ```

2. Generate normal authentication events:
   ```
   docker exec siem-pipeline_generator_1 python3 /scripts/generator.py
   ```

3. Generate brute-force attack simulation:
   ```
   docker exec siem-pipeline_generator_1 python3 /scripts/generator.py --mode brute-force
   ```

## Monitoring

- **Kibana**: Access at `http://localhost:5601`
- **Grafana**: Access at `http://localhost:3000` (default credentials: admin/admin)
- **Elasticsearch**: Access at `http://localhost:9200`

## Features Implemented

### Milestone 1 & 2
- Real-time log ingestion and analysis
- Authentication event monitoring
- Dashboard visualization
- Log parsing and indexing

### Milestone 3
- Brute-force attack detection and alerting
- Additional dashboard panels for security analytics
- Enhanced event logging and schema support

## Log Generator Usage

The generator supports multiple modes:

- **Normal mode** (default): Generates typical authentication events
- **Brute-force mode**: Generates a scenario with multiple failed login attempts from the same source

Use `--mode` argument to specify behavior:
```
python3 /scripts/generator.py --mode normal
python3 /scripts/generator.py --mode brute-force
```

## Security Dashboard

The Grafana dashboard contains several key panels for security monitoring:

1. **Total Authentication Events** - Overview of all events
2. **Successful/Failed Authentications** - Statistics on auth outcomes
3. **Successes and Failures Over Time** - Timeline view of authentication trends  
4. **Top Source IPs producing failures** - Identifies problematic IP addresses
5. **Raw Authentication Logs** - Full log data (for troubleshooting)
6. **Failed Logins by Source IP** - Detailed breakdown of failed attempts by source
7. **Failed Logins by Username** - Tracks which accounts are targeted
8. **Possible Brute-Force Sources** - Identifies potential brute-force attacks
9. **Authentication Events by Scenario** - Pie chart showing normal vs brute-force events
10. **Raw Security Events** - Complete log stream for in-depth analysis

## Implementation Details

### Architecture Diagram

```
[Generator] → [Logstash] → [Elasticsearch] 
         ← [Kibana] ← [Grafana]
```

This pipeline supports real-time ingestion of synthetic authentication events and provides visualization capabilities to detect security threats like brute-force attacks.

The system is designed for continuous operation with auto-restart policies for all components, providing a production-like environment for SIEM demonstration.