from ishchi_app.models import WorkDayMoney
from obyekt_app.models import Obyekt, WorkAmount


def calculate_worker_to_obyekt(workdaymoney_id):
    workdaymoney = WorkDayMoney.objects.get(id=workdaymoney_id)
    for work in workdaymoney.work_amount.all():
        # work.completed
        work_amount = WorkAmount.objects.get(id=work.job.id)
        work_amount.total_completed += work.completed
        work_amount.save()
        obyekt_data = work_amount.obyekt_set.values().first()
        # work.job.total_completed+=work.completed
        obyekt_data['real_dept'] = obyekt_data['real_dept']-work.completed*work_amount.service_price

        first_obyekt = work_amount.obyekt_set.first()
        for key, value in obyekt_data.items():
            setattr(first_obyekt, key, value)

        # Save the changes
        first_obyekt.save()