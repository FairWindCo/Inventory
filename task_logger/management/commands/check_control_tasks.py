import platform
import smtplib

from django.core.management import BaseCommand
from django.utils.timezone import now

from dictionary.models import ServerScheduledTask
from info.models import Server
from task_logger.models import TaskControl


def send_mail(message, config):
    SMTP_SERVER = config.get('server', '127.0.0.1')
    SMTP_PORT = config.get('port', 25)
    FROM_MAIL = config.get('from_mail', '').strip().lower()
    USER_MAIL = config.get('mail_user', '')
    PASS_MAIL = config.get('mail_pass', '')
    TO_MAIL = config.get('to_mail', "bspd@erc.ua").strip().lower()
    smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    if USER_MAIL:
        smtp.login(USER_MAIL, PASS_MAIL)
    smtp.sendmail(FROM_MAIL, TO_MAIL, message)


def send_mail_mime(message, config):
    msg = format_message(message, config)
    return send_mail(msg.as_string(), config)


def get_text_html_part(report: dict):
    plain_message = []
    html_tasks = []

    for group, reports in report.items():
        ok_task = []
        error_task = []
        not_run = []
        for task in reports:
            state = task['state']
            if state is None or state > 0:
                not_run.append(f"Завдання {task['task_code_name']} на сервері {task['server']}")
            else:
                if task['error_code']:
                    error_task.append(
                        f"Завдання {task['task_code_name']}  на сервері {task['server']} - завершена с ошибкой: {task['message']}")
                else:
                    ok_task.append(f"Завдання {task['task_code_name']}  на сервері {task['server']}")

        plain_message.append(f"Група завдань: {group}")
        html_tasks.append(f'<h2>Група завдань: {group}</h2>')
        plain_message.append('Виконані успішно:')
        html_tasks.append('<h3>Виконані успішно:</h3>')
        plain_message.extend(ok_task)
        html_tasks.append("<ul>")
        html_tasks.extend(map(lambda a: f'<li>{a}</li>', ok_task))
        html_tasks.append("</ul>")
        plain_message.append('ВИКОНАНІ З ПОМИЛКАМИ:')
        html_tasks.append('<h3>ВИКОНАНІ З ПОМИЛКАМИ:</h3>')
        plain_message.extend(error_task)
        html_tasks.append("<ul>")
        html_tasks.extend(map(lambda a: f'<li style:"color:red;">{a}</li>', error_task))
        html_tasks.append("</ul>")
        plain_message.append('НЕ ВИКОНАНІ:')
        html_tasks.append('<h3>НЕ ВИКОНАНІ:</h3>')
        plain_message.extend(not_run)
        html_tasks.append("<ul>")
        html_tasks.extend(map(lambda a: f'<li>{a}</li>', not_run))
        html_tasks.append("</ul>")

        return html_tasks, plain_message


def format_message(report: dict, config: dict):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    html_tasks, plain_message = get_text_html_part(report)

    part1 = MIMEText('\n'.join(plain_message), "plain")
    message = MIMEMultipart("alternative")
    message["Subject"] = "Звіт про автоматичні таски"
    html = """\
    <html>
      <body>        
        <div>
        {}
        </div>
      </body>
    </html>
    """.format(''.join(html_tasks))

    message["From"] = config.get('from_mail', '')
    message["To"] = config.get('to_mail', "bspd@erc.ua")

    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    return message


class Command(BaseCommand):
    help = 'Check tasks'

    def handle(self, *args, **options):
        from Inventarisation.settings import MAIL_SEND_REPORT
        report = {}
        try:
            server_name = Server.objects.get(name=platform.node())
            self_control_task = TaskControl.objects.get_or_create(code=1, host=server_name.id)
            self_control_task.last_execute = now()
            self_control_task.status = 1
            self_control_task.save()
        except Server.DoesNotExist:
            self_control_task = None

        for control in TaskControl.objects.order_by('control_group', 'code').all():
            need_notify = False
            if control.last_message is None:
                need_notify = True
            else:
                delta = now() - control.last_message
                need_notify = delta.total_seconds() > 12 * 60 * 60
            if control.control_group is not None:
                need_notify = control.control_group.send_message
            if need_notify:
                group_name = str(control.control_group)
                if group_name not in report:
                    report[group_name] = []
                if control.last_execute is None:
                    state = None
                else:
                    delta = now() - control.last_execute
                    shift = control.period * control.period_multiply
                    state = delta.total_seconds() - shift

                try:
                    task_desc = ServerScheduledTask.objects.get(code=control.code)
                    if task_desc.short_desc:
                        task_name = f'{task_desc.name} ({task_desc.short_desc})'
                    else:
                        task_name = f'{task_desc.name}'
                except ServerScheduledTask.DoesNotExist:
                    task_name = f'Код задачі: {control.code}'

                report[group_name].append({
                    'task_code_name': task_name,
                    'server': control.host.name,
                    'state': state,
                    'message': control.message,
                    'error_code': control.status,
                })
                control.last_message = now()
                control.save()
        print(report)
        send_mail_mime(report, MAIL_SEND_REPORT)
        if self_control_task:
            self_control_task.last_execute = now()
            self_control_task.status=0
            self_control_task.save()
