import pygame, sys, os
import assistant

# http://www.learningpython.com/2006/03/12/creating-a-game-in-python-using-pygame-part-one/
# TODO:
# Handle shift numkeys
# Allow holding down delete key
# Center window when too much text, eventually go onto new line
# add speech to text
# execute search on return key press
# create new class to display pods

def render_textrect(string, font, rect, text_color, background_color, justification=0):
    final_lines = []
    requested_lines = string.splitlines()
    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise TextRectException, "The word " + word + " is too long to fit in the rect passed."
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "  
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line
                else:
                    final_lines.append(accumulated_line)
                    accumulated_line = word + " "
            final_lines.append(accumulated_line)
        else:
            final_lines.append(requested_line)
    surface = pygame.Surface(rect.size)
    surface.fill(background_color)
    accumulated_height = 0
    for line in final_lines:
        if accumulated_height + font.size(line)[1] >= rect.height:
            raise TextRectException, "Once word-wrapped, the text string was too tall to fit in the rect."
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise TextRectException, "Invalid justification argument: " + str(justification)
        accumulated_height += font.size(line)[1]
    return surface

class search:

    def __init__(self, width=600,height=50):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (420,100)
        os.chdir("/Projects/EngineerAssistant")
        pygame.init()
        self.width = width
        self.originalheight = height
        self.height = height
        self.fillcolor = (40,40,40)
        self.fillcolor2 = (10,10,10)
        self.textcolor = (250,250,250)
        self.spacing = 4
        self.sidespacing = 8
        self.appendarea = self.height+self.spacing
        self.podheights = []

        self.shift = False
        self.key = ""
        self.string = ""

        self.font = pygame.font.SysFont("franklingothicbook",30)
        self.text = self.font.render(self.string,True,self.textcolor)
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME)
        self.screen.fill(self.fillcolor)

    def query(self):
        while True:
            for event in pygame.event.get():
                # Shift
                if (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and (event.key == 303 or event.key == 304):
                    if event.type == pygame.KEYDOWN:
                        self.shift = True
                    else:
                        self.shift = False
                # Quit
                if event.type == pygame.QUIT: 
                    sys.exit()
                # Get Key, add to string
                if event.type == pygame.KEYDOWN:
                    if event.key == 8 and len(self.string) != 0:
                        self.string = self.string[:-1]
                    elif event.key == 96:
                        self.string = assistant.speech2text()
                    elif event.key == 13:
                        return
                    else:
                        self.key = ""
                        if event.key <= 255:
                            self.key = chr(event.key - self.shift*32)
                        self.string += self.key
                # Update Text
                self.text = self.font.render(self.string,True,self.textcolor)
                # Clear Screen
                self.screen.fill(self.fillcolor)
                # Expand if text goes off screen (temporary fix)
                if self.text.get_width()+2*self.sidespacing > self.width:
                    self.screen = pygame.display.set_mode((self.text.get_width()+2*self.sidespacing, self.height), pygame.NOFRAME)
                # Draw Text
                self.screen.blit(self.text,(self.sidespacing,self.height//2 - self.text.get_height()//2))
                # Show
                pygame.display.flip()

    def getheight(self,pod):
        height = 0
        self.font = pygame.font.SysFont("franklingothicbook",16)
        text = self.font.render(pod.name.encode('ascii','ignore'),True,(0,0,0))
        height += text.get_height()
        self.font = pygame.font.SysFont("franklingothicbook",12)
        boxheight = 5
        while True:
            try:
                if type(pod.text) is unicode:
                    render_textrect(pod.text.encode('ascii','ignore'),self.font,pygame.Rect((0,0),(self.width,boxheight)),self.textcolor,self.fillcolor2)
                    height += boxheight
                elif type(pod.text) is str:
                    render_textrect(pod.text,self.font,pygame.Rect((0,0),(self.width,boxheight)),self.textcolor,self.fillcolor2)
                    height += boxheight
                break
            except:
                boxheight += 5
                if boxheight > 850:
                    break
        height += 2*self.spacing
        try:
            height += pygame.image.load(os.path.join('/Projects/EngineerAssistant', pod.img)).get_height()
        except:
            height += 330
        return height

    def displaypod(self,pod):
        self.font = pygame.font.SysFont("franklingothicbook",16)
        text = self.font.render(pod.name.encode('ascii','ignore'),True,self.textcolor)
        self.screen.blit(text,(self.sidespacing,self.appendarea))
        extradist = text.get_height() + self.spacing
        self.font = pygame.font.SysFont("franklingothicbook",12)
        boxheight = 5
        while True:
            try:
                if type(pod.text) is unicode:
                    text = render_textrect(pod.text.encode('ascii','ignore'),self.font,pygame.Rect((0,0),(self.width,boxheight)),self.textcolor,self.fillcolor2)
                    self.screen.blit(text,(self.sidespacing,self.appendarea+extradist))
                elif type(pod.text) is str:
                    text = render_textrect(pod.text,self.font,pygame.Rect((0,0),(self.width,boxheight)),self.textcolor,self.fillcolor2)
                    self.screen.blit(text,(self.sidespacing,self.appendarea+extradist))
                break
            except:
                boxheight += 5
                if boxheight > 850:
                    break
        extradist += boxheight + self.spacing
        if len(pod.img) != 0:
            self.image = pygame.image.load(os.path.join('/Projects/EngineerAssistant', pod.img))
        self.screen.blit(self.image,(self.sidespacing,self.appendarea+extradist))

    def displaypods(self,pods):
        self.height += 2*self.spacing
        for i, pod in enumerate(pods):
            self.podheights.append(self.getheight(pod))
            self.height += self.podheights[i] + self.spacing
            if self.height > 850:
                self.height -= (self.podheights[i] + self.spacing)
                i -= 1
                break
        self.numpods = i+1
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME)
        self.screen.fill(self.fillcolor)
        self.screen.blit(self.text,(self.sidespacing,self.originalheight//2 - self.text.get_height()//2))
        for j in range(self.numpods):
            self.displaypod(pods[j])
            self.appendarea += self.podheights[j] + self.spacing
        pygame.display.flip()


def waitforuser():
    while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == 13:
                    return

if __name__ == "__main__":
    while True:
        searchbar = search()
        searchbar.query()
        assistant.getintents(searchbar.string)
        assistant.runaction()
        searchbar.displaypods(assistant.pods)
        waitforuser()
        assistant.pods = []

