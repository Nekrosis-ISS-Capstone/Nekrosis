"""
export.py: Export the persistence methods to structured data (XML, JSON, or plist).
"""

import enum
import json
import plistlib

from xml.etree import ElementTree


class ExportPersistenceTypes(enum.Enum):
    XML:   str = "xml"
    JSON:  str = "json"
    PLIST: str = "plist"


class ExportPersistenceMethods:
    """
    Export the persistence methods to structured data (XML, JSON, or plist).

    Parameters:
    - persistence_methods: A list of persistence methods.
    - recommended_method: The recommended persistence method.
    - export_method: The export method (XML, JSON, or plist).
    """
    def __init__(self, persistence_methods: list, recommended_method: str, export_method: ExportPersistenceTypes = ExportPersistenceTypes.PLIST) -> None:
        self.persistence_methods = persistence_methods
        self.recommended_method = recommended_method
        self.export_method = export_method


    def export(self) -> str:
        if self.export_method == ExportPersistenceTypes.XML:
            return self._export_xml()
        elif self.export_method == ExportPersistenceTypes.JSON:
            return self._export_json()
        elif self.export_method == ExportPersistenceTypes.PLIST:
            return self._export_plist()

        raise ValueError(f"Unsupported export method: {self.export_method}")


    def _export_xml(self) -> str:
        """
        Export the persistence methods to an XML string.
        """
        root = ElementTree.Element("persistence_methods")
        recommended = ElementTree.SubElement(root, "recommended_method")
        recommended.text = self.recommended_method

        methods = ElementTree.SubElement(root, "methods")
        for method in self.persistence_methods:
            ElementTree.SubElement(methods, "method").text = method

        return ElementTree.tostring(root, encoding="unicode") + "\n"


    def _export_json(self) -> str:
        """
        Export the persistence methods to a JSON string.
        """
        return json.dumps({
            "persistence_methods": self.persistence_methods,
            "recommended_method": self.recommended_method
        }, indent=4) + "\n"


    def _export_plist(self) -> str:
        """
        Export the persistence methods to a plist string.
        """
        return plistlib.dumps({
            "persistence_methods": self.persistence_methods,
            "recommended_method": self.recommended_method
        }).decode("utf-8")
