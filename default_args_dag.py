def get_args(self, overrides=None):
    """
    These args should be used to set DAG.default_args, when DAG failures and SLAs are to be monitored with PagerDuty
    This alerting implementation directly integrates with PagerDuty Events API v2, avoiding the need for email alerting.

    An optional dict of overrides can be provided, which will update the returned default_args dict.
    """
    default_args = {
        'owner': self.owner,
        'email_on_failure': False,
        'email_on_retry': False,
        'on_failure_callback': self.pager_duty_incident_dag_failure
    }

    if overrides:
        default_args.update(overrides)

    return default_args‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍

    pager_duty = PagerDuty()

with DAG(
        DAG_ID,
        default_args=pager_duty.get_args(overrides={
            'sla': timedelta(hours=2)
        }),
        start_date=datetime(2018, 1, 1),
        schedule_interval='0 1 * * *',
        catchup=False,
        sla_miss_callback=pager_duty.pager_duty_incident_sla_miss,
) as dag:    