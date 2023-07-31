from model.kinematics import Kinematics


class AMR:
    """
    Represents an Autonomous Mobile Robot (AMR).

    Attributes:
        id (int): The unique identifier for the AMR.
        kinematics (Kinematics): The kinematics parameters for the AMR.
    """

    def __init__(self, amr_id: int, friendly_name: str, kinematics: Kinematics):
        """
        Initializes an AMR object with the given parameters.

        Args:
            amr_id (int): The unique identifier for the AMR.
            kinematics (Kinematics): The kinematics parameters for the AMR.
        """
        self.id = amr_id
        self.friendly_name = friendly_name
        self.kinematics = kinematics

    def __str__(self):
        """
        Returns a string representation of the AMR object.

        Returns:
            str: String representation of the AMR object.
        """
        return f"AMR {self.id} ({self.friendly_name}):\n    {self.kinematics}"

    def __eq__(self, other):
        """
        Comparison method to check if two AMR objects are equal based on their id.

        Args:
            other (AMR): Another AMR object to compare.

        Returns:
            bool: True if the AMR objects have the same id and kinematics, False otherwise.
        """
        if not isinstance(other, AMR):
            return False
        return self.id == other.id

    def __hash__(self):
        """
        Hash method based on the AMR id.

        Returns:
            int: The hash value of the AMR object based on its id and kinematics.
        """
        return hash(self.id)
