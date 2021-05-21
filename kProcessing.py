class keyInit:
    import pygame
    def isQuit(self):
        if '<Event(12-Quit {})>' in list(map(str, self.pygame.event.get())):
            return True
    def key(self, wasd=False):
        events=[None, None]
        keys=self.pygame.key.get_pressed()
        if keys[self.pygame.K_SPACE] or keys[self.pygame.K_q]:
            events[0]='fire'
        if keys[self.pygame.K_RIGHT] or keys[self.pygame.K_d]:
            events[1]='right'
        elif keys[self.pygame.K_LEFT] or keys[self.pygame.K_a]:
            events[1]='left'
        elif keys[self.pygame.K_DOWN] or keys[self.pygame.K_s]:
            events[1]='down'
        elif keys[self.pygame.K_UP] or keys[self.pygame.K_w]:
            events[1]='up'
        return events