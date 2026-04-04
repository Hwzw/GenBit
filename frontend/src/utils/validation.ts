const DNA_REGEX = /^[ATCGatcgNn]+$/;
const PROTEIN_REGEX = /^[ACDEFGHIKLMNPQRSTVWYacdefghiklmnpqrstvwy*]+$/;
const ACCESSION_REGEX = /^[A-Z]{1,2}_?\d{5,}(\.\d+)?$/;

export function isValidDNA(sequence: string): boolean {
  return DNA_REGEX.test(sequence.trim());
}

export function isValidProtein(sequence: string): boolean {
  return PROTEIN_REGEX.test(sequence.trim());
}

export function isValidAccession(accession: string): boolean {
  return ACCESSION_REGEX.test(accession.trim());
}
