def enqueue_incident(self, context):
    source = context['conf'].get('webserver', 'base_url')
    self.log.info(
        f"Enqueueing incident to PagerDuty: [summary: {self.summary}, "
        f"source: {source}, component: {self.component}, incident_class: {self.incident_class}]"
    )

    header = {
        'Content-Type': 'application/json'
    }
    payload = {
        'routing_key': self.integration_key,
        'event_action': 'trigger',
        'payload': {
            'summary': self.summary,
            'source': source,
            'severity': self.severity,
            'component': self.component,
            'class': self.incident_class,
            'custom_details': self.details
        },
        'links': self.links if self.links else self.default_links(context)
    }
    response = requests.post('https://events.pagerduty.com/v2/enqueue',
                             data=json.dumps(payload),
                             headers=header)

    self.log.info('enqueue incident response: %s', response)
    if not response.ok:
        raise AirflowException(f"PagerDuty trigger incident api call failed: {response.json()}")

    return response.json()['dedup_key']