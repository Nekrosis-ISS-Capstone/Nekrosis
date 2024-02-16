"""
error_wrapper.py: Wrapper for error handling.
"""

import sys
import logging
import threading
import subprocess


_ORIGINAL_SYS_EXCEPTHOOK    = sys.excepthook
_ORIGINAL_THREAD_EXCEPTHOOK = threading.excepthook


class CaptureExceptions:
    """
    Allow exceptions to be captured and logged.
    Currently only supports main thread and threading-based exceptions.
    """
    def __init__(self) -> None:
        pass


    def _set_custom_traceback_handler(self) -> None:
        """
        Implement custom traceback handler.
        """

        def custom_excepthook(type, value, tb) -> None:
            """
            Custom traceback handler.
            """
            logging.error("Uncaught exception", exc_info=(type, value, tb))


        def custom_thread_excepthook(args) -> None:
            """
            Custom thread exception handler.
            """
            logging.error("Uncaught exception", exc_info=args)


        sys.excepthook       = custom_excepthook
        threading.excepthook = custom_thread_excepthook


    def _restore_original_traceback_handler(self) -> None:
        """
        Restore original traceback handler.
        """
        sys.excepthook       = _ORIGINAL_SYS_EXCEPTHOOK
        threading.excepthook = _ORIGINAL_THREAD_EXCEPTHOOK


    def start(self) -> None:
        """
        Start capturing exceptions.
        """
        self._set_custom_traceback_handler()


    def stop(self) -> None:
        """
        Stop capturing exceptions.
        """
        self._restore_original_traceback_handler()


class SubprocessErrorLogging:
    """
    Display subprocess error output.
    """
    def __init__(self, process: subprocess.CompletedProcess) -> None:
        self.process = process


    def __str__(self) -> str:
        """
        Display subprocess error output in formatted string.

        Format:

        Command: <command>
        Return Code: <return code>
        Standard Output:
            <standard output line 1>
            <standard output line 2>
            ...
        Standard Error:
            <standard error line 1>
            <standard error line 2>
            ...
        """
        output = "Error: Subprocess failed.\n"
        output += f"    Command: {self.process.args}\n"
        output += f"    Return Code: {self.process.returncode}\n"
        output += f"    Standard Output:\n"
        output += self._format_output(self.process.stdout)
        output += f"    Standard Error:\n"
        output += self._format_output(self.process.stderr)

        return output


    def _format_output(self, output: str) -> str:
        """
        Format output.
        """
        if not output:
            return "        None\n"

        return "\n".join([f"        {line}" for line in output.split("\n") if line not in ["", "\n"]])


    def log(self) -> None:
        """
        Log subprocess error output.
        """
        logging.error(str(self))

