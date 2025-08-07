# URL Shortener Microservices Project

This is a Kubernetes-based microservices project that implements a simple URL shortener with full observability. It includes a backend (Flask), frontend (React), Redis for caching, and monitoring setup with Prometheus and Grafana.

---

## 🚀 Features

- URL shortening service with Flask backend and Redis for fast lookup
- Frontend interface built in React
- Kubernetes-native deployment using Helm
- Horizontal Pod Autoscaler (HPA) for backend
- Prometheus metrics exposed by the backend and visualized via Grafana

---

## 🧱 Architecture Overview

```
+-----------+       +-----------+       +-------------+
| Frontend  | <---> |  Backend  | <---> |    Redis    |
+-----------+       +-----------+       +-------------+
                          |
                     Exposes /metrics
                          |
                    +-----------+
                    | Prometheus|
                    +-----------+
                          |
                    +-----------+
                    |  Grafana  |
                    +-----------+
```

---

## 📦 Helm Installation

```bash
helm install url-shortener ./helm
```

To uninstall:

```bash
helm uninstall url-shortener
```

---

## 📈 Grafana Dashboards

1. **Backend CPU Usage Per Pod**  
   Query used:

   ```promql
   sum by (pod) (
     rate(container_cpu_usage_seconds_total{pod=~"backend.*"}[1m])
   )
   ```

2. **Custom Dashboards**  
   Feel free to add memory usage, HPA current vs desired, etc.

---

## ⚙️ HPA Configuration

Backend `deployment.yaml` snippet:

```yaml
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "500m"
    memory: "256Mi"
```

Applied HPA:

```bash
kubectl autoscale deployment backend --cpu-percent=50 --min=1 --max=5
```

---

## 📊 Metrics Setup

Prometheus annotations on backend deployment:

```yaml
annotations:
  prometheus.io/scrape: "true"
  prometheus.io/port: "5000"
  prometheus.io/path: "/metrics"
```

---

## 📁 Repository Structure

```
.
├── backend/
├── frontend/
├── k8s/
└── README.md
```

---

## 📌 Requirements

- Minikube or local K8s cluster
- Helm v3
- kubectl
- Prometheus & Grafana installed via Helm

---

## 🧠 Author Notes

Built as a personal DevOps project to demonstrate:

- Kubernetes deployment using Helm
- Microservices architecture
- Monitoring & observability using Prometheus & Grafana
- Scaling with HPA

---

_Last updated: 2025-08-07_
