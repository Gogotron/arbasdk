from pygame import display, event, joystick, JOYBUTTONUP, JOYBUTTONDOWN, K_LEFT, K_RIGHT, K_DOWN, K_UP, JOYHATMOTION, JOYAXISMOTION
from time import time
from .abstract import AbstractEvents


class SystemEvents(AbstractEvents):
    # Hat mapping[axis][value] = Pressed key or 'released" in case we must consult the previous value
    hat_mapping = {0: {-1: 'left', 1: 'right', 0: 'released'},
                   1: {-1: 'down', 1: 'up', 0: 'released'}}

    # Joystick keys mapping
    joy_mapping = {K_LEFT: 'left', K_RIGHT: 'right', K_DOWN: 'down', K_UP: 'up'}

    def __init__(self):
        super(SystemEvents, self).__init__()
        display.init()
        joystick.init()
        self.hats = []
        for j in range(joystick.get_count()):
            joy = joystick.Joystick(j)
            joy.init()
            hats = []
            for hat in range(joy.get_numhats()):
                hats.append([0, 0])
            self.hats.append(hats)

    def get(self):
        """
        Get events event from pygame to dictionaries
        :param event: a pygame.Event object from pygame
        :return: dict of type {'key': 'left', 'device': keyboard', 'pressed': True, 'time': 1485621689.548}
        """
        user_events = []
        for e in event.get():
            if e.type in [JOYBUTTONUP, JOYBUTTONDOWN]:
                key = self.joy_mapping[e.button] if e.button in self.joy_mapping else e.button
                user_events.append({'key': key,
                                    'device': {'type': 'joystick', 'id': e.joy},
                                    'pressed': e.type == JOYBUTTONDOWN,
                                    'time': time()})

            elif e.type == JOYHATMOTION:
                if len(e.value) != 2:
                    print("pygame system events has received a joystick event with unsupported number of hat directions: {}".format(len(e.value)))
                    continue

                for key in range(2):
                    if self.hats[e.joy][e.hat][key] != e.value[key]:
                        # Transform the hat motions into button presses with a custom mapping
                        type = self.hat_mapping[key][e.value[key]]
                        if type == 'released':
                            # The previous stored direction has been released
                            type = self.hat_mapping[key][self.hats[e.joy][e.hat][key]]
                            pressed = False
                        else:
                            pressed = True

                        user_events.append({'key': type,
                                            'device': {'type': 'joystick', 'id': e.joy},
                                            'pressed': pressed,
                                            'time': time()})
                        self.hats[e.joy][e.hat][key] = e.value[key]

            elif e.type == JOYAXISMOTION:
                continue

        return user_events



    # def run(self):
    #     """
    #     Run the event manager that redistributes duplicated events to user and SDK, and TODO gathers all events
    #     """
    #     self.running = True
    #     while self.running:
    #         self.system_events = self._get()  # Get the system event list
    #         if self._runtime_control:
    #             # Check for the touch toggling signal
    #             for ev in self.system_events:
    #                 if ev.type == JOYBUTTONDOWN and ev.button in self._arbalet.joystick['touch']:
    #                     self._arbalet.touch.toggle_touch()
    #                 if ev.type in [MOUSEBUTTONDOWN, MOUSEBUTTONUP]:
    #                     self._arbalet.handle_mouse_event(ev)
    #                 if ev.type == QUIT:
    #                     if self._arbalet.arbasim is not None:
    #                         self._arbalet.arbasim.close()
    #                     self.running = False
    #                     break
    #         self._rate.sleep()
