/**
 * Modelo base para respuestas de la API
 */
export interface ApiResponse<T> {
  data: T;
  message: string;
  success: boolean;
  status: number;
}

/**
 * Modelo para respuestas de error de la API
 */
export interface ApiError {
  message: string;
  status: number;
  errors?: { [key: string]: string[] };
}

/**
 * Modelo para paginación
 */
export interface PaginationParams {
  page: number;
  limit: number;
  sort?: string;
  order?: 'asc' | 'desc';
}

/**
 * Modelo para respuestas paginadas
 */
export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}