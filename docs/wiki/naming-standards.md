# Estándares de Nombramiento - PrevMora

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Estándares Generales](#estándares-generales)
3. [Backend (Python/FastAPI)](#backend-pythonfastapi)
4. [Frontend (Next.js/TypeScript)](#frontend-nextjstypescript)
5. [Base de Datos](#base-de-datos)
6. [Ejemplos Prácticos](#ejemplos-prácticos)
7. [Referencias](#referencias)

## Introducción

Este documento establece los estándares de nombramiento para el proyecto **PrevMora**, una solución de microfinanzas enfocada en la gestión de cobranza temprana de créditos. 

Los estándares definidos siguen las mejores prácticas oficiales de los lenguajes y frameworks utilizados, garantizando consistencia, legibilidad y mantenibilidad del código.

### Justificación

La implementación de estándares de nombramiento consistentes proporciona:
- **Legibilidad**: Código más fácil de leer y entender
- **Mantenibilidad**: Facilita el mantenimiento y evolución del código
- **Colaboración**: Mejora la comunicación entre desarrolladores
- **Profesionalismo**: Sigue las mejores prácticas de la industria

## Estándares Generales

### Principios Fundamentales
1. **Claridad sobre brevedad**: Los nombres deben ser descriptivos y claros
2. **Consistencia**: Mantener el mismo estilo en todo el proyecto
3. **Contexto apropiado**: Los nombres deben ser apropiados para su contexto
4. **Evitar abreviaciones**: Excepto para convenciones ampliamente conocidas

### Lenguajes Soportados
- **Español**: Para nombres de dominio y conceptos de negocio
- **Inglés**: Para nombres técnicos y de programación

## Backend (Python/FastAPI)

Basado en [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/) y [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/).

### Archivos y Módulos
```python
# ✅ Correcto
portfolio.py
credit_management.py
excel_loader_service.py

# ❌ Incorrecto
Portfolio.py
CreditManagement.py
ExcelLoaderService.py
```

**Regla**: `snake_case` para nombres de archivos y módulos.

### Clases
```python
# ✅ Correcto
class Portfolio:
class CreditManager:
class ExcelLoaderService:

# ❌ Incorrecto
class portfolio:
class credit_manager:
class excelLoaderService:
```

**Regla**: `PascalCase` para nombres de clases.

### Funciones y Métodos
```python
# ✅ Correcto
def get_portfolio_by_id():
def calculate_installment_amount():
def process_credit_application():

# ❌ Incorrecto
def GetPortfolioById():
def calculateInstallmentAmount():
def ProcessCreditApplication():
```

**Regla**: `snake_case` para funciones y métodos.

### Variables y Parámetros
```python
# ✅ Correcto
portfolio_id = 123
client_name = "Juan Pérez"
total_amount = 15000.00

# ❌ Incorrecto
PortfolioId = 123
ClientName = "Juan Pérez"
TotalAmount = 15000.00
```

**Regla**: `snake_case` para variables y parámetros.

### Constantes
```python
# ✅ Correcto
MAX_CREDIT_AMOUNT = 50000.00
DEFAULT_INTEREST_RATE = 0.12
API_VERSION = "v1"

# ❌ Incorrecto
max_credit_amount = 50000.00
defaultInterestRate = 0.12
```

**Regla**: `UPPER_SNAKE_CASE` para constantes.

### Rutas de API
```python
# ✅ Correcto
@router.get("/portfolios")
@router.post("/portfolios/{portfolio_id}/credits")
@router.put("/clients/{client_id}")

# ❌ Incorrecto
@router.get("/Portfolios")
@router.post("/portfolios/{portfolioId}/credits")
@router.put("/Clients/{ClientId}")
```

**Regla**: `kebab-case` para rutas, `snake_case` para parámetros de ruta.

### Modelos Pydantic
```python
# ✅ Correcto
class PortfolioCreate(BaseModel):
    name: str
    manager_id: int
    creation_date: datetime

class CreditResponse(BaseModel):
    credit_id: int
    client_name: str
    total_amount: float
```

**Regla**: `PascalCase` para clases, `snake_case` para atributos.

## Frontend (Next.js/TypeScript)

Basado en [TypeScript Style Guide](https://typescript-lang.org/docs/handbook/declaration-files/do-s-and-don-ts.html) y [Next.js Conventions](https://nextjs.org/docs/getting-started/project-structure).

### Archivos y Directorios
```typescript
// ✅ Correcto - Componentes
components/PortfolioCard.tsx
components/CreditForm.tsx
components/ui/Button.tsx

// ✅ Correcto - Páginas
pages/portfolios/index.tsx
pages/credits/[id].tsx
pages/admin/dashboard.tsx

// ✅ Correcto - Utilidades
utils/formatCurrency.ts
hooks/usePortfolio.ts
services/apiClient.ts

// ❌ Incorrecto
components/portfolio-card.tsx
pages/Portfolios/Index.tsx
utils/format_currency.ts
```

**Reglas**:
- `PascalCase` para componentes React (`.tsx`)
- `camelCase` para utilidades y servicios (`.ts`)
- `kebab-case` para directorios de páginas cuando sea necesario

### Componentes React
```typescript
// ✅ Correcto
const PortfolioCard: React.FC<PortfolioCardProps> = ({ portfolio }) => {
  return <div>...</div>;
};

const CreditForm: React.FC = () => {
  return <form>...</form>;
};

// ❌ Incorrecto
const portfolioCard = () => { ... };
const credit_form = () => { ... };
```

**Regla**: `PascalCase` para componentes React.

### Interfaces y Types
```typescript
// ✅ Correcto
interface Portfolio {
  id: number;
  name: string;
  managerId: number;
  creationDate: string;
}

type CreditStatus = 'active' | 'paid' | 'overdue';

interface PortfolioCardProps {
  portfolio: Portfolio;
  onSelect: (id: number) => void;
}

// ❌ Incorrecto
interface portfolio { ... }
type credit_status = string;
interface PortfolioCardprops { ... }
```

**Regla**: `PascalCase` para interfaces y types, `camelCase` para propiedades.

### Variables y Funciones
```typescript
// ✅ Correcto
const portfolioList = useState<Portfolio[]>([]);
const handleCreditSubmit = (data: CreditData) => { ... };
const isLoading = false;

// ❌ Incorrecto
const PortfolioList = useState([]);
const HandleCreditSubmit = () => { ... };
const is_loading = false;
```

**Regla**: `camelCase` para variables y funciones.

### Constantes
```typescript
// ✅ Correcto
const API_BASE_URL = 'http://localhost:8000';
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const CREDIT_STATUSES = ['active', 'paid', 'overdue'] as const;

// ❌ Incorrecto
const apiBaseUrl = 'http://localhost:8000';
const max_file_size = 5242880;
```

**Regla**: `UPPER_SNAKE_CASE` para constantes exportadas.

### CSS Classes (TailwindCSS)
```typescript
// ✅ Correcto
<div className="portfolio-card bg-white shadow-lg rounded-lg p-4">
<button className="btn btn-primary hover:btn-primary-focus">

// ❌ Incorrecto
<div className="PortfolioCard">
<div className="portfolio_card">
```

**Regla**: `kebab-case` para clases CSS personalizadas, mantener convenciones de TailwindCSS y DaisyUI.

## Base de Datos

### Tablas
```sql
-- ✅ Correcto
portfolios
credits
clients
installments
reconciliations

-- ❌ Incorrecto
Portfolio
Credit
client_table
```

**Regla**: `snake_case` en plural para nombres de tablas.

### Columnas
```sql
-- ✅ Correcto
portfolio_id
client_name
creation_date
total_amount
interest_rate

-- ❌ Incorrecto
PortfolioId
ClientName
CreationDate
totalAmount
```

**Regla**: `snake_case` para nombres de columnas.

### Claves Primarias
```sql
-- ✅ Correcto
id (para claves primarias simples)
portfolio_id (para claves foráneas)

-- ❌ Incorrecto
PortfolioID
portfolio_ID
```

**Regla**: `id` para claves primarias, `tabla_id` para claves foráneas.

### Índices
```sql
-- ✅ Correcto
idx_portfolios_manager_id
idx_credits_client_id
idx_installments_due_date

-- ❌ Incorrecto
PortfolioManagerIndex
idx_Credits_ClientId
```

**Regla**: `idx_tabla_columna(s)` en `snake_case`.

## Ejemplos Prácticos

### Ejemplo Completo: Gestión de Portafolios

#### Backend (FastAPI)
```python
# models/portfolio.py
class Portfolio(Base):
    __tablename__ = "portfolios"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    manager_id = Column(Integer, ForeignKey("managers.id"))
    creation_date = Column(DateTime, default=datetime.utcnow)

# schemas/portfolio.py
class PortfolioBase(BaseModel):
    name: str
    manager_id: int

class PortfolioCreate(PortfolioBase):
    pass

class PortfolioResponse(PortfolioBase):
    id: int
    creation_date: datetime

# controllers/portfolio.py
class PortfolioController:
    def __init__(self, repository: PortfolioRepository):
        self.repository = repository
    
    async def get_portfolio_by_id(self, portfolio_id: int) -> Portfolio:
        return await self.repository.get_by_id(portfolio_id)
    
    async def create_portfolio(self, portfolio_data: PortfolioCreate) -> Portfolio:
        return await self.repository.create(portfolio_data)

# routes/v1/portfolio.py
@router.get("/portfolios/{portfolio_id}", response_model=PortfolioResponse)
async def get_portfolio(
    portfolio_id: int,
    controller: PortfolioController = Depends()
):
    return await controller.get_portfolio_by_id(portfolio_id)
```

#### Frontend (Next.js/TypeScript)
```typescript
// types/portfolio.ts
export interface Portfolio {
  id: number;
  name: string;
  managerId: number;
  creationDate: string;
}

export interface PortfolioCreateRequest {
  name: string;
  managerId: number;
}

// services/portfolioService.ts
export class PortfolioService {
  private static readonly API_BASE = '/api/credit-management/v1';
  
  static async getPortfolioById(portfolioId: number): Promise<Portfolio> {
    const response = await fetch(`${this.API_BASE}/portfolios/${portfolioId}`);
    return response.json();
  }
  
  static async createPortfolio(data: PortfolioCreateRequest): Promise<Portfolio> {
    const response = await fetch(`${this.API_BASE}/portfolios`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  }
}

// components/PortfolioCard.tsx
interface PortfolioCardProps {
  portfolio: Portfolio;
  onEdit: (id: number) => void;
  onDelete: (id: number) => void;
}

export const PortfolioCard: React.FC<PortfolioCardProps> = ({
  portfolio,
  onEdit,
  onDelete,
}) => {
  const formattedDate = formatDate(portfolio.creationDate);
  
  const handleEditClick = () => {
    onEdit(portfolio.id);
  };
  
  const handleDeleteClick = () => {
    onDelete(portfolio.id);
  };
  
  return (
    <div className="portfolio-card card bg-base-100 shadow-xl">
      <div className="card-body">
        <h2 className="card-title">{portfolio.name}</h2>
        <p className="text-sm text-gray-600">Creado: {formattedDate}</p>
        <div className="card-actions justify-end">
          <button 
            className="btn btn-primary btn-sm"
            onClick={handleEditClick}
          >
            Editar
          </button>
          <button 
            className="btn btn-error btn-sm"
            onClick={handleDeleteClick}
          >
            Eliminar
          </button>
        </div>
      </div>
    </div>
  );
};

// hooks/usePortfolios.ts
export const usePortfolios = () => {
  const [portfolios, setPortfolios] = useState<Portfolio[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const fetchPortfolios = async () => {
    setIsLoading(true);
    try {
      const data = await PortfolioService.getAllPortfolios();
      setPortfolios(data);
      setError(null);
    } catch (err) {
      setError('Error al cargar portafolios');
    } finally {
      setIsLoading(false);
    }
  };
  
  return {
    portfolios,
    isLoading,
    error,
    fetchPortfolios,
  };
};
```

## Referencias

### Documentación Oficial

#### Python/FastAPI
- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)
- [Pydantic Naming Strategy](https://docs.pydantic.dev/latest/concepts/alias/)
- [SQLAlchemy Naming Conventions](https://docs.sqlalchemy.org/en/20/core/constraints.html#constraint-naming-conventions)

#### TypeScript/Next.js
- [TypeScript Coding Guidelines](https://github.com/Microsoft/TypeScript/wiki/Coding-guidelines)
- [Next.js Project Structure](https://nextjs.org/docs/getting-started/project-structure)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/docs/basic/getting-started/naming_conventions/)
- [TailwindCSS Naming Conventions](https://tailwindcss.com/docs/utility-first)

#### Base de Datos
- [PostgreSQL Naming Conventions](https://www.postgresql.org/docs/current/sql-syntax-lexical.html#SQL-SYNTAX-IDENTIFIERS)
- [Database Design Best Practices](https://www.sqlstyle.guide/)

### Estándares de la Comunidad
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

**Documento creado**: Septiembre 2025  
**Última actualización**: Septiembre 2025  
**Versión**: 1.0  
**Mantenido por**: Equipo de desarrollo PrevMora
