export interface Client {
  id: number;
  created_at: string | null;
  updated_at: string | null;
  name: string;
  document: string;
  email: string;
  phone: string;
  address: string;
  zone: string;
  status: string;
}

export interface ClientsResponse {
  total: number;
  page: number;
  page_size: number;
  pages: number;
  items: Client[];
}

export interface Credit {
  id: number;
  client_id: number;
  disbursement_amount: number;
  payment_reference: string;
  interest_rate: number;
  total_quotas: number;
  disbursement_date: string;
  credit_state: string;
  created_at: string;
  updated_at: string;
  installments: Installment[];
}

export interface Installment {
  id: number;
  credit_id: number;
  installment_state: string;
  installments_number: number;
  installments_value: string;
  due_date: string;
  payment_date: string | null;
  created_at: string;
  updated_at: string;
  portfolio: PortfolioManagement[];
}

export interface PortfolioManagement {
  id: number;
  installment_id: number;
  manager_id: number;
  contact_method: string;
  contact_result: string;
  management_date: string;
  observation: string | null;
  payment_promise_date: string | null;
  created_at: string;
  updated_at: string;
}

export interface Alert {
  id: number;
  credit_id: number;
  client_id: number;
  alert_type: string;
  manually_generated: boolean;
  alert_date: string;
  created_at: string;
  updated_at: string;
}

export interface Reconciliation {
  id: number;
  transaction_date: string;
  payment_reference: string;
  payment_amount: number;
  payment_channel: string;
  observation: string | null;
  created_at: string;
  updated_at: string;
}

export interface ClientCompleteData {
  id: number;
  name: string;
  document: string;
  email: string;
  phone: string;
  address: string;
  zone: string;
  status: string;
  created_at: string | null;
  updated_at: string | null;
  credits: Credit[];
  alerts: Alert[];
  reconciliations: Reconciliation[];
  total_credits: number;
  total_installments: number;
  total_portfolio_managements: number;
  total_alerts: number;
  total_reconciliations: number;
}
