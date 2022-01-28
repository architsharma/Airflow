def pager_duty_incident_dag_failure(self, context):
    operator = PagerDutyIncidentOperator(
        task_id='pager_duty_incident_dag_failure',
        monitoring_enabled=self.monitoring_enabled,
        integration_key=self.integration_key(),
        summary=f"Airflow DAG failure: {context['task_instance']}",
        component='Airflow Worker',
        incident_class='DAG Failure',
        details=self._dag_failure_details(context),
        links=PagerDutyIncidentOperator.default_links(context)  # Create links from context of failed task
    )
    return operator.execute(context=context)

def pager_duty_incident_sla_miss(self, dag, task_list, blocking_task_list, slas, blocking_tis):
    context = self._get_context_from_slas(slas)
    operator = PagerDutyIncidentOperator(
        task_id='pager_duty_incident_sla_miss',
        monitoring_enabled=self.monitoring_enabled,
        integration_key=self.integration_key(),
        summary=f"Airflow SLA miss: <DAG: {dag.dag_id}>",
        component='Airflow Scheduler',
        incident_class='SLA Miss',
        details=self._sla_miss_details(context, dag, task_list, blocking_task_list),
        links=PagerDutyIncidentOperator.default_links(context)  # Create links for context of missed SLA
    )

    return operator.execute(context=context)