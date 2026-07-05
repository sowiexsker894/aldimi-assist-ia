export interface DniConfirmedFields {
  nombre: string;
  apellido_paterno: string;
  apellido_materno: string;
  dni_number: string;
  sexo: string;
  nacionalidad: string;
  fecha_nacimiento: string;
  fecha_expiracion: string;
  lugar_nacimiento: string;
  direccion: string;
}

export interface DniFieldsConfirmedEvent {
  sessionId: string;
  fields: DniConfirmedFields;
  warnings: string[];
}

export interface DniPatientSavedEvent {
  patientId: number;
  documentId: number;
}

export type DniOcrMode = 'prefill' | 'savePatient';

export const emptyDniFields = (): DniConfirmedFields => ({
  nombre: '',
  apellido_paterno: '',
  apellido_materno: '',
  dni_number: '',
  sexo: '',
  nacionalidad: '',
  fecha_nacimiento: '',
  fecha_expiracion: '',
  lugar_nacimiento: '',
  direccion: '',
});

export const strField = (v: unknown): string =>
  v == null || String(v) === 'null' ? '' : String(v);

export function fullNameFromDniFields(f: DniConfirmedFields): string {
  const parts = [f.nombre, f.apellido_paterno, f.apellido_materno]
    .map((p) => p.trim())
    .filter(Boolean);
  return parts.join(' ');
}

export function patientPayloadFromDniFields(f: DniConfirmedFields, fullName: string) {
  return {
    full_name: fullName,
    dni: f.dni_number || undefined,
    primer_nombre: f.nombre || undefined,
    primer_apellido: f.apellido_paterno || undefined,
    segundo_apellido: f.apellido_materno || undefined,
    sexo: f.sexo || undefined,
    nacionalidad: f.nacionalidad || undefined,
    fecha_nacimiento: f.fecha_nacimiento || undefined,
    direccion: f.direccion || undefined,
  };
}

export function dniSavePayload(f: DniConfirmedFields): Record<string, unknown> {
  return {
    nombre: f.nombre || null,
    apellido_paterno: f.apellido_paterno || null,
    apellido_materno: f.apellido_materno || null,
    dni_number: f.dni_number || null,
    sexo: f.sexo || null,
    nacionalidad: f.nacionalidad || null,
    fecha_nacimiento: f.fecha_nacimiento || null,
    fecha_expiracion: f.fecha_expiracion || null,
    lugar_nacimiento: f.lugar_nacimiento || null,
    direccion: f.direccion || null,
  };
}
