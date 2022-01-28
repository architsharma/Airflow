def data_is_fresh_branch(**context):
    # Set downstream success or alert task based on string boolean result of data freshness check
    is_fresh = context['ti'].xcom_pull('check_data_freshness', key='is_fresh')
    return 'data_freshness_success' if is_fresh else 'data_freshness_failure_alert'

check_data_freshness = ...

data_is_fresh = BranchPythonOperator(
    task_id='data_is_fresh',
    python_callable=data_is_fresh_branch,
    provide_context=True,
)

data_freshness_success = DummyOperator(task_id='data_freshness_success')

data_freshness_failure_alert = PagerDutyIncidentOperator(
    task_id='data_freshness_failure_alert',
    monitoring_enabled=pager_duty.monitoring_enabled,
    integration_key='{{ pagerduty_integration_key() }}',
    summary='Dataset freshness check failed',
    component='Test DAG',
    incident_class='Freshness Check',
    details='Dataset freshness check failed for filename: ' \
            '{{ task_instance.xcom_pull("check_data_freshness", key="return_value") }}'
)

check_data_freshness >> data_is_fresh
data_is_fresh >> data_freshness_success
data_is_fresh >> data_freshness_failure_alert‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍