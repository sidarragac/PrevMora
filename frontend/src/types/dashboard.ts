// Tipos para el dashboard basados en la documentación del backend

export interface PaginationParams {
  page: number;
  page_size: number;
}

// Alertas
export interface Alert {
  id: number | null;
  created_at: string | null;
  updated_at: string | null;
  credit_id: number;
  client_id: number;
  alert_type: string;
  manually_generated: boolean;
  alert_date: string;
}

export interface AlertList {
  total: number;
  page: number;
  page_size: number;
  pages: number;
  items: Alert[];
}

// Créditos
export interface Credit {
  id: number;
  created_at: string | null;
  updated_at: string | null;
  client_id: number;
  disbursement_amount: number;
  payment_reference: string;
  interest_rate: number;
  total_quotas: number;
  disbursement_date: string;
  credit_state: string;
}

export interface CreditList {
  total: number;
  page: number;
  page_size: number;
  pages: number;
  items: Credit[];
}

// Cuotas
export interface Installment {
  id: number | null;
  created_at: string | null;
  updated_at: string | null;
  credit_id: number;
  installment_state: string;
  installments_number: number;
  installments_value: string;
  due_date: string;
  payment_date: string | null;
}

export interface InstallmentList {
  total: number;
  page: number;
  page_size: number;
  pages: number;
  items: Installment[];
}

// Gestión de Cartera
export interface Portfolio {
  id: number | null;
  created_at: string | null;
  updated_at: string | null;
  installment_id: number;
  manager_id: number;
  contact_method: string;
  contact_result: string;
  management_date: string;
  observation: string | null;
  payment_promise_date: string | null;
}

export interface PortfolioList {
  total: number;
  page: number;
  page_size: number;
  pages: number;
  items: Portfolio[];
}

// Conciliaciones
export interface Reconciliation {
  id: number | null;
  created_at: string | null;
  updated_at: string | null;
  payment_channel: string;
  payment_reference: string;
  payment_amount: number;
  transaction_date: string;
  observation: string | null;
}

export interface ReconciliationList {
  total: number;
  page: number;
  page_size: number;
  pages: number;
  items: Reconciliation[];
}

// Gestores
export interface Manager {
  id: number | null;
  created_at: string | null;
  updated_at: string | null;
  name: string;
  manager_zone: string;
}

export interface ManagerList {
  total: number;
  page: number;
  page_size: number;
  pages: number;
  items: Manager[];
}

// Tipos para el dashboard
export interface DashboardStats {
  totalClients: number;
  totalCredits: number;
  totalAlerts: number;
  totalInstallments: number;
  totalPortfolioManagements: number;
  totalReconciliations: number;
  totalManagers: number;
}

export interface DashboardData {
  stats: DashboardStats;
  recentAlerts: Alert[];
  recentInstallments: Installment[];
  recentPortfolioManagements: Portfolio[];
  recentReconciliations: Reconciliation[];
}
