class PointsSystem:
    def __init__(self, initial_points=0):
        self.points = initial_points
        self.multiplier = 1.0
    
    def add_points(self, points):
        """Add points with current multiplier applied"""
        added = points * self.multiplier
        self.points += added
        return added
    
    def subtract_points(self, points):
        """Subtract points with current multiplier applied"""
        subtracted = points * self.multiplier
        self.points -= subtracted
        return subtracted
    
    def set_multiplier(self, multiplier):
        """Set the points multiplier"""
        self.multiplier = multiplier
    
    def get_points(self):
        """Get current points total"""
        return self.points
    
    def reset_points(self):
        """Reset points to zero"""
        self.points = 0