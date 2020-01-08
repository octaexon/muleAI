import abc
import threading


class BasePart(abc.ABC):
    """Common interface for vehicle parts."""
    @abc.abstractmethod
    def start(self):
        """Starts part components."""
        raise NotImplementedError

    @abc.abstractmethod
    def transform(self, state):
        """Transforms vehicle state.

        Args:
            state: dictionary storing elements comprising vehicle state
        """
        raise NotImplementedError

    @abc.abstractmethod
    def stop(self):
        """Stops part components."""
        raise NotImplementedError


class ThreadComponent:
    """Stoppable threading mixin.

    Attributes:
        target: function to be repeated evaluated in separate thread
        thread: thread object
        event: flag to stop thread
    """
    def __init__(self, target, **kwargs):
        """Create thread holding target function.

        Args:
            target: function to be repeated evaluated in separate thread
            kwargs: arguments to be passed to target

        """
        self.target = target
        self.thread = threading.Thread(target=self._repeated_target,
                                       kwargs=kwargs)
        self.event = threading.Event()

    def start(self):
        """Starts thread."""
        self.thread.start()

    def stop(self):
        """Stops thread."""
        self.event.set()
        self.thread.join()

    def _repeated_target(self, **kwargs):
        """Enables repeated evaluation of target function."""
        while not self.event.is_set():
            self.target(**kwargs)
