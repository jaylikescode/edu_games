# UI Components for Planet Latin
import pygame
from config import Colors, GameConfig

class Button:
    def __init__(self, x, y, width, height, text, font, color=Colors.UI_BACKGROUND, 
                 text_color=Colors.TEXT_WHITE, hover_color=None, border_color=Colors.WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color
        self.hover_color = hover_color or (min(255, color[0] + 30), min(255, color[1] + 30), min(255, color[2] + 30))
        self.border_color = border_color
        self.is_hovered = False
        self.is_clicked = False
        
        # Render text
        self.text_surface = font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
    
    def handle_event(self, event):
        """Handle mouse events"""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.is_clicked = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                was_clicked = self.is_clicked and self.rect.collidepoint(event.pos)
                self.is_clicked = False
                return was_clicked
        return False
    
    def draw(self, screen):
        """Draw the button"""
        # Choose color based on state
        current_color = self.hover_color if self.is_hovered else self.color
        
        # Draw button background
        pygame.draw.rect(screen, current_color, self.rect, border_radius=5)
        pygame.draw.rect(screen, self.border_color, self.rect, 2, border_radius=5)
        
        # Draw text
        screen.blit(self.text_surface, self.text_rect)


class ScrollableList:
    def __init__(self, x, y, width, height, items, font, item_height=40):
        self.rect = pygame.Rect(x, y, width, height)
        self.items = items
        self.font = font
        self.item_height = item_height
        self.scroll_offset = 0
        self.max_visible_items = height // item_height
        self.selected_index = -1
        self.hovered_index = -1
        
        # Scrollbar
        self.scrollbar_width = 20
        self.scrollbar_rect = pygame.Rect(x + width - self.scrollbar_width, y, 
                                        self.scrollbar_width, height)
        self.scrollbar_handle_height = max(20, (self.max_visible_items / len(items)) * height)
        self.scrollbar_dragging = False
        self.drag_start_y = 0
    
    def handle_event(self, event):
        """Handle mouse events"""
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            if self.rect.collidepoint(event.pos):
                # Calculate hovered item
                relative_y = mouse_y - self.rect.y
                item_index = (relative_y // self.item_height) + self.scroll_offset
                self.hovered_index = item_index if 0 <= item_index < len(self.items) else -1
            else:
                self.hovered_index = -1
            
            # Handle scrollbar dragging
            if self.scrollbar_dragging:
                delta_y = mouse_y - self.drag_start_y
                self.scroll_offset = max(0, min(len(self.items) - self.max_visible_items,
                                              int(delta_y / self.rect.height * len(self.items))))
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.scrollbar_rect.collidepoint(event.pos):
                    self.scrollbar_dragging = True
                    self.drag_start_y = event.pos[1]
                elif self.rect.collidepoint(event.pos):
                    # Select item
                    mouse_x, mouse_y = event.pos
                    relative_y = mouse_y - self.rect.y
                    item_index = (relative_y // self.item_height) + self.scroll_offset
                    if 0 <= item_index < len(self.items):
                        self.selected_index = item_index
                        return item_index
            
            elif event.button == 4:  # Mouse wheel up
                if self.rect.collidepoint(event.pos):
                    self.scroll_offset = max(0, self.scroll_offset - 1)
            elif event.button == 5:  # Mouse wheel down
                if self.rect.collidepoint(event.pos):
                    self.scroll_offset = min(len(self.items) - self.max_visible_items, 
                                           self.scroll_offset + 1)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.scrollbar_dragging = False
        
        return -1
    
    def draw(self, screen):
        """Draw the scrollable list"""
        # Draw background
        pygame.draw.rect(screen, Colors.UI_BACKGROUND, self.rect)
        pygame.draw.rect(screen, Colors.WHITE, self.rect, 2)
        
        # Draw items
        visible_items = self.items[self.scroll_offset:self.scroll_offset + self.max_visible_items]
        for i, item in enumerate(visible_items):
            item_y = self.rect.y + i * self.item_height
            item_rect = pygame.Rect(self.rect.x, item_y, 
                                  self.rect.width - self.scrollbar_width, self.item_height)
            
            actual_index = i + self.scroll_offset
            
            # Highlight selected or hovered item
            if actual_index == self.selected_index:
                pygame.draw.rect(screen, Colors.EASY_LEVEL, item_rect)
            elif actual_index == self.hovered_index:
                pygame.draw.rect(screen, Colors.LIGHT_GRAY, item_rect)
            
            # Draw item text
            if isinstance(item, dict):
                text = item.get('name', str(item))
            else:
                text = str(item)
            
            text_surface = self.font.render(text, True, Colors.TEXT_BLACK)
            text_rect = text_surface.get_rect(center=(item_rect.centerx, item_rect.centery))
            screen.blit(text_surface, text_rect)
            
            # Draw separator line
            if i < len(visible_items) - 1:
                pygame.draw.line(screen, Colors.GRAY, 
                               (self.rect.x, item_y + self.item_height), 
                               (self.rect.right - self.scrollbar_width, item_y + self.item_height))
        
        # Draw scrollbar if needed
        if len(self.items) > self.max_visible_items:
            self.draw_scrollbar(screen)
    
    def draw_scrollbar(self, screen):
        """Draw the scrollbar"""
        # Scrollbar track
        pygame.draw.rect(screen, Colors.DARK_GRAY, self.scrollbar_rect)
        
        # Scrollbar handle
        handle_y = self.scrollbar_rect.y + (self.scroll_offset / len(self.items)) * self.rect.height
        handle_rect = pygame.Rect(self.scrollbar_rect.x, handle_y, 
                                self.scrollbar_width, self.scrollbar_handle_height)
        pygame.draw.rect(screen, Colors.LIGHT_GRAY, handle_rect)
        pygame.draw.rect(screen, Colors.WHITE, handle_rect, 1)
    
    def get_selected_item(self):
        """Get the currently selected item"""
        if 0 <= self.selected_index < len(self.items):
            return self.items[self.selected_index]
        return None


class TextDisplay:
    def __init__(self, x, y, width, height, font, text_color=Colors.TEXT_WHITE, 
                 background_color=None, border_color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text_color = text_color
        self.background_color = background_color
        self.border_color = border_color
        self.text_lines = []
        self.line_height = font.get_height() + 2
    
    def set_text(self, text):
        """Set the text content, automatically wrapping lines"""
        words = text.split(' ')
        self.text_lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            text_width = self.font.size(test_line)[0]
            
            if text_width <= self.rect.width - 20:  # 10px padding on each side
                current_line = test_line
            else:
                if current_line:
                    self.text_lines.append(current_line)
                current_line = word
        
        if current_line:
            self.text_lines.append(current_line)
    
    def draw(self, screen):
        """Draw the text display"""
        # Draw background
        if self.background_color:
            pygame.draw.rect(screen, self.background_color, self.rect)
        
        # Draw border
        if self.border_color:
            pygame.draw.rect(screen, self.border_color, self.rect, 2)
        
        # Draw text lines
        y_offset = self.rect.y + 10  # Top padding
        for line in self.text_lines:
            if y_offset + self.line_height > self.rect.bottom - 10:  # Bottom padding
                break
            
            text_surface = self.font.render(line, True, self.text_color)
            screen.blit(text_surface, (self.rect.x + 10, y_offset))  # Left padding
            y_offset += self.line_height


class MenuManager:
    def __init__(self):
        self.components = []
        self.active = True
    
    def add_component(self, component):
        """Add a UI component to the manager"""
        self.components.append(component)
    
    def handle_event(self, event):
        """Handle events for all components"""
        results = []
        for component in self.components:
            if hasattr(component, 'handle_event'):
                result = component.handle_event(event)
                if result is not None and result != -1 and result != False:
                    results.append((component, result))
        return results
    
    def draw(self, screen):
        """Draw all components"""
        for component in self.components:
            component.draw(screen)
    
    def clear(self):
        """Clear all components"""
        self.components.clear()
