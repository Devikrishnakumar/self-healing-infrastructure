# Self-Healing Infrastructure

## Project Overview

Self-Healing Infrastructure is a Docker-based infrastructure monitoring and recovery project designed to detect service failures and restore services with minimal manual intervention.

The project uses Prometheus to monitor infrastructure metrics, Alertmanager to manage alerts, Flask to receive alert notifications, and Ansible to execute recovery operations.

The recovery workflow is designed to restart an unhealthy NGINX container and verify that the service becomes available again.

## Objectives

- Monitor NGINX service health.
- Collect infrastructure metrics using Prometheus.
- Configure alert rules for service failures.
- Receive alerts through a Flask webhook.
- Automate recovery using Ansible.
- Run all components using Docker Compose.

## Technologies Used

| Technology | Purpose |
|---|---|
| Docker | Containerization |
| Docker Compose | Multi-container management |
| NGINX | Web server |
| Prometheus | Infrastructure monitoring |
| NGINX Prometheus Exporter | Metric collection |
| Alertmanager | Alert management |
| Python Flask | Webhook service |
| Ansible | Automated recovery |
| Linux / Ubuntu | Execution environment |

## Architecture

```text
          NGINX Web Server
                 |
                 v
       NGINX Prometheus Exporter
                 |
                 v
             Prometheus
                 |
                 v
            Alertmanager
                 |
                 v
           Flask Webhook
                 |
                 v
          Ansible Playbook
                 |
                 v
       Restart NGINX Container
                 |
                 v
          Service Recovery
```

## Project Structure

```text
self-healing-infrastructure/
│
├── alertmanager/
│   └── alertmanager.yml
│
├── ansible/
│   └── recover-nginx.yml
│
├── nginx/
│   └── default.conf
│
├── prometheus/
│   ├── prometheus.yml
│   └── alert-rules.yml
│
├── webhook/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── screenshots/
├── docs/
├── docker-compose.yml
└── .gitignore
```

## How It Works

1. **Monitoring:** Prometheus collects metrics from the NGINX Prometheus Exporter.
2. **Alert Configuration:** Prometheus evaluates configured alert rules to identify service failures.
3. **Alert Management:** Alertmanager is configured to forward alerts to the Flask webhook.
4. **Webhook Processing:** Flask receives alert notifications and identifies NGINX failure alerts.
5. **Automated Recovery:** Flask executes the Ansible recovery playbook.
6. **Service Restoration:** Ansible restarts the NGINX Docker container and checks whether the service responds successfully.

## Installation and Execution

### Prerequisites

- Docker Desktop
- WSL 2 with Ubuntu
- Docker Compose
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Devikrishnakumar/self-healing-infrastructure.git
cd self-healing-infrastructure
```

### 2. Start the Infrastructure

```bash
docker compose up -d --build
```

### 3. Check Running Containers

```bash
docker compose ps
```

### 4. View Container Logs

```bash
docker compose logs -f
```

## Access the Services

| Service | URL |
|---|---|
| NGINX | http://localhost:8081 |
| Prometheus | http://localhost:9090 |
| Alertmanager | http://localhost:9093 |
| NGINX Exporter | http://localhost:9113/metrics |
| Flask Webhook Health | http://localhost:5000/health |

## Recovery Testing

The Flask webhook and Ansible recovery workflow were tested using a simulated NGINX failure alert.

The following command sends a simulated firing alert to the webhook:

```bash
docker compose exec webhook python -c 'import json,urllib.request; data={"alerts":[{"status":"firing","labels":{"alertname":"NginxDown"}}]}; req=urllib.request.Request("http://localhost:5000/alert",data=json.dumps(data).encode(),headers={"Content-Type":"application/json"},method="POST"); print(urllib.request.urlopen(req).read().decode())'
```

Expected response:

```json
{
  "results": [
    {
      "action": "recovery_completed",
      "alert": "NginxDown"
    }
  ]
}
```

Verify NGINX availability:

```bash
curl -I http://localhost:8081
```

Expected result:

```text
HTTP/1.1 200 OK
```

The Ansible recovery playbook was also executed successfully, restarting the NGINX container and verifying its HTTP response.

**Testing note:** The Flask webhook → Ansible → Docker → NGINX recovery path was successfully verified using a simulated alert. The complete automatic Prometheus-to-Alertmanager-to-webhook alert-triggering path has not yet been verified.

## Benefits

- Reduces manual infrastructure recovery effort.
- Improves service availability.
- Provides centralized monitoring.
- Automates container recovery operations.
- Demonstrates practical DevOps and infrastructure automation concepts.
- Provides a foundation for more advanced self-healing systems.

## Future Enhancements

- Complete end-to-end automatic alert-triggered recovery.
- Add Telegram or email notifications.
- Monitor multiple services and containers.
- Add Grafana dashboards.
- Implement recovery history and reporting.
- Extend the solution to cloud infrastructure.

## Author

**Devi Krishnakumar**

GitHub: https://github.com/Devikrishnakumar

Repository: https://github.com/Devikrishnakumar/self-healing-infrastructure

---

*This project was developed as part of DevOps practical learning and infrastructure automation.*
