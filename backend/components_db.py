"""
Electronics Components Database
Comprehensive database of electronic components for circuit design
"""
from sqlalchemy import Column, Integer, String, Text, Float, JSON
from database import Base


class Component(Base):
    __tablename__ = "components"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(200), nullable=False, index=True)
    part_number = Column(String(100), nullable=True, index=True)
    category    = Column(String(100), nullable=False, index=True)
    subcategory = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    specs       = Column(JSON, nullable=True)   # key-value specs dict
    package     = Column(String(100), nullable=True)
    voltage     = Column(String(100), nullable=True)
    current     = Column(String(100), nullable=True)
    datasheet   = Column(String(500), nullable=True)
    tags        = Column(String(500), nullable=True)  # comma-separated

    def to_dict(self):
        return {
            "id":          self.id,
            "name":        self.name,
            "part_number": self.part_number,
            "category":    self.category,
            "subcategory": self.subcategory,
            "description": self.description,
            "specs":       self.specs,
            "package":     self.package,
            "voltage":     self.voltage,
            "current":     self.current,
            "datasheet":   self.datasheet,
            "tags":        self.tags,
        }
