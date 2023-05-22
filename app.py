import json
import logging
import requests
from kubernetes import client, config
from prometheus_client import start_http_server, Summary, Counter

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up Prometheus metrics
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
EVENTS_SENT = Counter('events_sent_total', 'Total number of events sent')


try:
    # Try to load the in-cluster configuration
    config.load_incluster_config()
except config.ConfigException:
    # If it fails, load the kubeconfig file
    config.load_kube_config()

v1 = client.CoreV1Api()

def send_event(event):
    # URL to send the POST request to
    url = 'https://ntfy.sh/dmarsgaltu'

    # Measure the time taken to send the event
    with REQUEST_TIME.time():
        # Send POST request
        response = requests.post(url, json=event)

    # Check if the request was successful
    if response.status_code == 200:
        # Increment the counter of events sent
        EVENTS_SENT.inc()
    else:
        logging.error(f'Failed to send event: {response.text}')

def get_events(sent_events):
    # Fetch events from Kubernetes API
    events = v1.list_event_for_all_namespaces(watch=False)

    # Parse events
    for event in events.items:
        event_info = {
            'Created': event.metadata.creation_timestamp.isoformat() if event.metadata.creation_timestamp else None,
            'Name': event.metadata.name,
            'Namespace': event.metadata.namespace,
            'Message': event.message,
            'Reason': event.reason,
            'Source': event.source.component,
            'First seen': event.first_timestamp.isoformat() if event.first_timestamp else None,
            'Last seen': event.last_timestamp.isoformat() if event.last_timestamp else None,
            'Count': event.count,
            'Type': event.type
        }

        # Create a unique identifier for the event
        event_id = (event_info['Name'], event_info['Last seen'])

        # If the event has already been sent, skip it
        if event_id in sent_events:
            continue

        # Add the event's identifier to the set of sent events
        sent_events.add(event_id)

        yield event_info

if __name__ == "__main__":
    # Start Prometheus server
    start_http_server(8000)

    # Set of identifiers of events that have been sent
    sent_events = set()

    while True:
        # Get events and send each one
        for event in get_events(sent_events):
            send_event(event)
