# PrevMora Frontend

Este es un proyecto [Next.js](https://nextjs.org) creado con [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## 🚀 Inicio Rápido

Primero, ejecuta el servidor de desarrollo:

```bash
npm run dev
# o
yarn dev
# o
pnpm dev
# o
bun dev
```

Abre [http://localhost:3000](http://localhost:3000) en tu navegador para ver el resultado.

Puedes comenzar a editar la página modificando `app/page.tsx`. La página se actualiza automáticamente mientras editas el archivo.

## 📋 Reglas del Proyecto

### ESLint Configuration

Este proyecto utiliza reglas estrictas de ESLint para mantener la calidad del código:

- **Preferencias de funciones**: Se requieren funciones flecha (`prefer-arrow-callback`)
- **Plantillas de string**: Se requieren template literals (`prefer-template`)
- **Punto y coma**: Obligatorio al final de las declaraciones (`semi`)
- **Comillas**: Se utilizan comillas simples (`quotes: 'single'`)
- **Convención de nombres de archivos**: Los archivos TypeScript/React deben usar kebab-case (`check-file/filename-naming-convention`)

### Prettier Configuration

Configuración de formateo automático del código:

- **Punto y coma**: Habilitado (`semi: true`)
- **Comillas simples**: Habilitadas (`singleQuote: true`)
- **Ancho de tabulación**: 2 espacios (`tabWidth: 2`)
- **Coma final**: Habilitada para ES5 (`trailingComma: "es5"`)

#### Orden de Imports

El proyecto mantiene un orden específico de imports:

1. **React y Next.js** (primero)
2. **Módulos de terceros**
3. **Componentes** (`@/components/*`)
4. **Hooks** (`@/hooks/*`)
5. **Librerías** (`@/libs/*`)
6. **Otros imports del proyecto** (`@/*`)
7. **Imports relativos** (`./*`)

- Separación automática entre grupos de imports
- Ordenamiento automático de especificadores

### Plugins Utilizados

- **@trivago/prettier-plugin-sort-imports**: Ordenamiento automático de imports
- **prettier-plugin-tailwindcss**: Formateo automático de clases de Tailwind CSS

## 🎨 Características del Proyecto

Este proyecto utiliza [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) para optimizar y cargar automáticamente [Geist](https://vercel.com/font), una nueva familia de fuentes para Vercel.

## 📚 Aprende Más

Para aprender más sobre Next.js, consulta los siguientes recursos:

- [Documentación de Next.js](https://nextjs.org/docs) - aprende sobre las características y API de Next.js.
- [Aprende Next.js](https://nextjs.org/learn) - un tutorial interactivo de Next.js.

Puedes revisar [el repositorio de GitHub de Next.js](https://github.com/vercel/next.js) - ¡tus comentarios y contribuciones son bienvenidos!

## 🚀 Despliegue en Vercel

La forma más fácil de desplegar tu aplicación Next.js es usar [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) de los creadores de Next.js.

Consulta nuestra [documentación de despliegue de Next.js](https://nextjs.org/docs/app/building-your-application/deploying) para más detalles.

## 🛠️ Scripts Disponibles

```bash
# Desarrollo
npm run dev

# Construcción para producción
npm run build

# Iniciar servidor de producción
npm start

# Linting
npm run lint

# Formateo de código
npm run format
```

## 📁 Estructura del Proyecto

```
src/
├── app/           # App Router de Next.js 13+
├── components/    # Componentes reutilizables
├── hooks/         # Custom hooks
└── types/         # Definiciones de tipos TypeScript
```

## 🔧 Configuración del Editor

Para una mejor experiencia de desarrollo, se recomienda configurar tu editor con:

- **ESLint**: Para linting automático
- **Prettier**: Para formateo automático
- **TypeScript**: Para verificación de tipos

### VS Code Configuration

El proyecto incluye configuración automática de VS Code en `.vscode/settings.json`:

- **Formateo automático**: Al guardar con Prettier
- **Linting automático**: Corrección automática de ESLint al guardar
- **Organización de imports**: Automática al guardar
- **Tamaño de tabulación**: 2 espacios (coincide con Prettier)
- **Validación de archivos**: TypeScript, JavaScript, React
- **Convención de nombres**: kebab-case para archivos `.ts` y `.tsx`

### Snippets Personalizados

Snippets de React configurados para kebab-case que convierten automáticamente el nombre del archivo:

- **`rfc`**: Componente funcional completo con interface de props
- **`rfcs`**: Componente funcional con useState hook
- **`rfce`**: Componente funcional con useEffect hook
- **`rfc-simple`**: Componente funcional simple sin props

**Ejemplo de uso**: Si creas un archivo `user-profile.tsx` y usas `rfc`, el snippet generará automáticamente:

```tsx
export const UserProfile: React.FC<UserProfileProps> = ({ ... }) => {
  // El nombre se convierte de kebab-case a PascalCase automáticamente
};
```

**Transformación automática**:

- `user-profile.tsx` → `UserProfile`
- `my-component.tsx` → `MyComponent`
- `header-nav.tsx` → `HeaderNav`
- `user-controller.tsx` → `UserController`
