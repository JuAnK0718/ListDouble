# models.py - Domain models for the veterinary clinic


from datetime import datetime


class Orion:
    """
    Represents the species/type of an animal patient.
    Named after the Orion constellation — a reference point in the cosmos.
    """

    def __init__(self, species_id: str, species_name: str, average_lifespan: float):
        self.__species_id = species_id
        self.__species_name = species_name
        self.__average_lifespan = average_lifespan

    # ── Getters ────────────────────────────────────────────────

    @property
    def species_id(self):
        return self.__species_id

    @property
    def species_name(self):
        return self.__species_name

    @property
    def average_lifespan(self):
        return self.__average_lifespan

    def __str__(self):
        return f"{self.__species_name} (ID: {self.__species_id})"


# ─────────────────────────────────────────────────────────────────────────────


class Pulsar:
    """
    Represents an animal patient registered in the clinic.
    Named after Pulsar stars — unique, rhythmic, and alive.
    """

    def __init__(self, patient_id: str, name: str, age: float,
                 weight: float, species: Orion, owner_name: str, owner_phone: str):
        self.__patient_id = patient_id
        self.__name = name
        self.__age = age
        self.__weight = weight
        self.__species = species
        self.__owner_name = owner_name
        self.__owner_phone = owner_phone
        self.__medical_history = []     # List of strings describing past treatments

    # ── Getters ────────────────────────────────────────────────

    @property
    def patient_id(self):
        return self.__patient_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        self.__age = value

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        self.__weight = value

    @property
    def species(self):
        return self.__species

    @property
    def owner_name(self):
        return self.__owner_name

    @owner_name.setter
    def owner_name(self, value):
        self.__owner_name = value

    @property
    def owner_phone(self):
        return self.__owner_phone

    @owner_phone.setter
    def owner_phone(self, value):
        self.__owner_phone = value

    @property
    def medical_history(self):
        return list(self.__medical_history)

    def add_medical_note(self, note: str):
        """Append a note to this patient's medical history."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.__medical_history.append(f"[{timestamp}] {note}")

    def __str__(self):
        return (f"ID: {self.__patient_id} | {self.__name} | "
                f"{self.__species.species_name} | Dueño: {self.__owner_name}")


# ─────────────────────────────────────────────────────────────────────────────


class Vortex:
    """
    Represents a scheduled appointment in the clinic.
    Named after Vortex — a swirling force that captures attention.
    """

    PENDING = "Pendiente"
    COMPLETED = "Completada"
    CANCELLED = "Cancelada"

    def __init__(self, appointment_id: str, patient: Pulsar,
                 date: str, reason: str, veterinarian: str):
        self.__appointment_id = appointment_id
        self.__patient = patient
        self.__date = date
        self.__reason = reason
        self.__veterinarian = veterinarian
        self.__status = Vortex.PENDING

    # ── Getters / Setters ──────────────────────────────────────

    @property
    def appointment_id(self):
        return self.__appointment_id

    @property
    def patient(self):
        return self.__patient

    @property
    def date(self):
        return self.__date

    @property
    def reason(self):
        return self.__reason

    @property
    def veterinarian(self):
        return self.__veterinarian

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        if value in [Vortex.PENDING, Vortex.COMPLETED, Vortex.CANCELLED]:
            self.__status = value

    def __str__(self):
        return (f"Cita {self.__appointment_id} | {self.__patient.name} | "
                f"{self.__date} | {self.__status}")
