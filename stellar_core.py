# stellar_core.py - Main controller (business logic layer)


from nebula_list import NebulaList
from models import Orion, Pulsar, Vortex


class StellarCore:
    """
    Central controller of the veterinary clinic system.
    Manages patients and appointments using NebulaList (doubly linked list).
    Named StellarCore — the engine at the heart of a star.
    """

    def __init__(self):
        self.__patients = NebulaList()          # Doubly linked list of Pulsar (patients)
        self.__appointments = NebulaList()      # Doubly linked list of Vortex (appointments)
        self.__species_catalog = {}             # Dict of Orion objects keyed by species_id
        self.__patient_counter = 1
        self.__appointment_counter = 1
        self.__load_default_species()
        self.__load_sample_data()

    # ── Species ────────────────────────────────────────────────

    def __load_default_species(self):
        """Preload common species into the catalog."""
        default_species = [
            Orion("SP001", "Perro",   15.0),
            Orion("SP002", "Gato",    14.0),
            Orion("SP003", "Conejo",   8.0),
            Orion("SP004", "Tortuga", 50.0),
            Orion("SP005", "Ave",      5.0),
        ]
        for sp in default_species:
            self.__species_catalog[sp.species_id] = sp

    def get_all_species(self):
        return list(self.__species_catalog.values())

    def get_species_by_id(self, species_id):
        return self.__species_catalog.get(species_id)

    # ── Patients ───────────────────────────────────────────────

    def __load_sample_data(self):
        """Insert demo patients and appointments for testing."""
        dog = self.__species_catalog["SP001"]
        cat = self.__species_catalog["SP002"]
        rabbit = self.__species_catalog["SP003"]

        p1 = Pulsar("PAC001", "Rigel",   3.0, 8.5,  dog,    "Carlos Medina",   "3101234567")
        p2 = Pulsar("PAC002", "Lyra",    5.0, 4.2,  cat,    "Sandra Torres",   "3209876543")
        p3 = Pulsar("PAC003", "Comet",   2.0, 1.8,  rabbit, "Diego Ríos",      "3157654321")
        p4 = Pulsar("PAC004", "Altair",  7.0, 6.1,  dog,    "Lucia Vargas",    "3001112233")
        p5 = Pulsar("PAC005", "Celeste", 1.5, 3.9,  cat,    "Andrés Morales",  "3144445566")

        p1.add_medical_note("Vacuna antirrábica aplicada.")
        p2.add_medical_note("Desparasitación interna completada.")
        p4.add_medical_note("Revisión general sin novedad.")

        for patient in [p1, p2, p3, p4, p5]:
            self.__patients.insert_at_end(patient)
        self.__patient_counter = 6

        a1 = Vortex("APT001", p1, "2025-08-10", "Control anual",      "Dra. Solano")
        a2 = Vortex("APT002", p2, "2025-08-11", "Vacunación",         "Dr. Céspedes")
        a3 = Vortex("APT003", p3, "2025-08-12", "Revisión digestiva", "Dra. Solano")
        a2.status = Vortex.COMPLETED

        for appt in [a1, a2, a3]:
            self.__appointments.insert_at_end(appt)
        self.__appointment_counter = 4

    # ── Patient CRUD ───────────────────────────────────────────

    def register_patient(self, name, age, weight, species_id, owner_name, owner_phone):
        """Create and store a new Pulsar patient at the end of the list."""
        species = self.get_species_by_id(species_id)
        if not species:
            return None, "Especie no encontrada."
        patient_id = f"PAC{self.__patient_counter:03d}"
        new_patient = Pulsar(patient_id, name, float(age), float(weight),
                             species, owner_name, owner_phone)
        self.__patients.insert_at_end(new_patient)
        self.__patient_counter += 1
        return new_patient, "Paciente registrado exitosamente."

    def delete_patient(self, patient_id):
        """Remove a patient node from the doubly linked list."""
        removed = self.__patients.delete_by_id(patient_id)
        return removed

    def get_all_patients(self):
        return self.__patients.traverse_forward()

    def get_patients_reversed(self):
        return self.__patients.traverse_backward()

    def search_patient_by_id(self, patient_id):
        return self.__patients.search_by_id(patient_id)

    def search_patients_by_name(self, name):
        return self.__patients.search_by_name(name)

    def add_medical_note(self, patient_id, note):
        """Append a medical note to a patient without rebuilding the list."""
        patient = self.search_patient_by_id(patient_id)
        if patient:
            patient.add_medical_note(note)
            return True
        return False

    def total_patients(self):
        return self.__patients.get_size()

    # ── Appointment CRUD ───────────────────────────────────────

    def schedule_appointment(self, patient_id, date, reason, veterinarian):
        """Create a new Vortex appointment linked to an existing patient."""
        patient = self.search_patient_by_id(patient_id)
        if not patient:
            return None, "Paciente no encontrado."
        appt_id = f"APT{self.__appointment_counter:03d}"
        new_appt = Vortex(appt_id, patient, date, reason, veterinarian)
        self.__appointments.insert_at_end(new_appt)
        self.__appointment_counter += 1
        return new_appt, "Cita agendada exitosamente."

    def get_all_appointments(self):
        return self.__appointments.traverse_forward()

    def update_appointment_status(self, appt_id, new_status):
        current = self.__appointments.head
        while current:
            if current.data.appointment_id == appt_id:
                current.data.status = new_status
                return True
            current = current.next
        return False

    def total_appointments(self):
        return self.__appointments.get_size()

    def get_list_structure_info(self):
        """Return metadata about the doubly linked list for visualization."""
        patients = self.__patients.traverse_forward()
        info = {
            "size": self.__patients.size,
            "head": patients[0].name if patients else "—",
            "tail": patients[-1].name if patients else "—",
        }
        return info
