import json

from urllib3.exceptions import NewConnectionError
from winrm.exceptions import WinRMError, WinRMTransportError, WinRMOperationTimeoutError, AuthenticationError, \
    BasicAuthDisabledError, InvalidCredentialsError
import logging
import winrm

from remoting.data_type_convertion import convert_to_lines


class MySession(winrm.Session):

    def run_cmd(self, command, args=()):
        shell_id = self.protocol.open_shell(codepage=866)
        command_id = self.protocol.run_command(shell_id, command, args)
        rs = winrm.Response(self.protocol.get_command_output(shell_id, command_id))
        self.protocol.cleanup_command(shell_id, command_id)
        self.protocol.close_shell(shell_id)
        return rs


def connect(host, user, password, ):
    if host and user:
        try:
            powershell_session = MySession(host, auth=(user, password), transport='ntlm')
            # p = winrm.Protocol(endpoint=host,
            #                    transport='ntlm',
            #                    username=user,
            #                    password=password,
            #                    server_cert_validation='ignore',
            #                    message_encryption='auto')
            # powershell_session.protocol = p
            return powershell_session
        except BasicAuthDisabledError as e:
            logging.error(f"REMOTING ERROR: {e}")
        except InvalidCredentialsError as e:
            logging.error(f"REMOTING ERROR: {e}")
        except AuthenticationError as e:
            logging.error(f"REMOTING ERROR: {e}")
        except NewConnectionError as _:
            logging.error(f"cod n`t connect")
        except ConnectionRefusedError as e:
            logging.error(f"Connection Refused ERROR: {e}")
        except ConnectionError as e:
            logging.error(f"Connection ERROR: {e}")
        except Exception as e:
            logging.error(f"ERROR: {e}")
    else:
        logging.error(f"NO PASSWORD for {host}")


def execute_ps(session, command, codepage='cp866'):
    if session is None:
        return None
    try:
        res = session.run_ps(command)
        if res.status_code != 0:
            logging.warning(f"WARNING REMOTING ERROR: {res.status_code}")
            logging.warning(res.std_err.decode(codepage))
            return None
        else:
            return res.std_out.decode(codepage)
    except WinRMError as e:
        logging.error(f"REMOTING ERROR: {e}")
    except WinRMTransportError as e:
        logging.error(f"REMOTING TRANSPORT ERROR: {e}")
    except WinRMOperationTimeoutError as e:
        logging.error(f"REMOTING TIMEOUT ERROR: {e}")
    except NewConnectionError as _:
        logging.error(f"cod n`t connect")
    except ConnectionRefusedError as e:
        logging.error(f"Connection Refused ERROR: {e}")
    except ConnectionError as e:
        logging.error(f"Connection ERROR: {e}")
    except Exception as e:
        logging.error(f"ERROR: {e}")


def execute_cmd(session, command, codepage='cp866'):
    if session is None:
        return None
    try:
        res = session.run_cmd(command)
        if res.status_code != 0:
            logging.warning(f"WARNING REMOTING ERROR: {res.status_code}")
            return None
        else:
            return res.std_out.decode(codepage)
    except WinRMError as e:
        logging.error(f"REMOTING ERROR: {e}")
    except WinRMTransportError as e:
        logging.error(f"REMOTING TRANSPORT ERROR: {e}")
    except WinRMOperationTimeoutError as e:
        logging.error(f"REMOTING TIMEOUT ERROR: {e}")
    except ConnectionRefusedError as e:
        logging.error(f"Connection Refused ERROR: {e}")
    except ConnectionError as e:
        logging.error(f"Connection ERROR: {e}")
    except NewConnectionError as _:
        logging.error(f"cod n`t connect")
    except Exception as e:
        logging.error(f"{e}")


def powershell(session, command):
    data = execute_ps(session, command, codepage='cp866')
    if data:
        return convert_to_lines(data)


def powershell_json(session, command):
    data = execute_ps(session, command, codepage='cp866')
    if data:
        return json.loads(data)
